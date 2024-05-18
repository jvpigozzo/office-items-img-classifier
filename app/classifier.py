import os
import io
import json
import requests
from PIL import Image
from transformers import ViltProcessor, ViltForQuestionAnswering

from models import Label, Model
from utils import encode_image
from dotenv import load_dotenv
from database import get_database
from prompts import PromptGenerator

from schemas.label import serialize_labels

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

db = get_database()


class ModelPipeline:
    def __init__(self, prompt_template: str, img_path: str, model_name: str):
        self.prompt_template = prompt_template
        self.img_path = img_path
        self.model_name = model_name
        self.model = db["models"].find_one({"name": model_name})
        if self.model_name == "vilt-b32-finetuned-vqa":
            self.processor = ViltProcessor.from_pretrained(
                "dandelin/vilt-b32-finetuned-vqa"
            )
            self.model_instance = ViltForQuestionAnswering.from_pretrained(
                "dandelin/vilt-b32-finetuned-vqa"
            )
        self.labels = self.get_labels()

    def process(self):
        if self.model_name == "gpt-4-turbo":
            return self.gpt4turbo()
        elif self.model_name == "vilt-b32-finetuned-vqa":
            return self.vilt()
        else:
            raise ValueError("Unsupported model name")

    def get_labels(self):
        labels = serialize_labels(list(db.labels.find()))
        return {item["id"]: item["name"] for item in labels}

    def vilt(self):
        processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        model = ViltForQuestionAnswering.from_pretrained(
            "dandelin/vilt-b32-finetuned-vqa"
        )

        with open(self.img_path, mode="rb") as file:
            content = file.read()

        image = Image.open(io.BytesIO(content))
        encoding = processor(image, self.prompt_template, return_tensors="pt")
        outputs = model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        label = model.config.id2label[idx]
        for key, value in self.labels.items():
            if value == label:
                result = {"label_id": key}
            else:
                None
        return result

    def gpt4turbo(self):
        with open(self.img_path, mode="rb") as file:
            content = file.read()

        image_str = encode_image(content)
        prompt = PromptGenerator(
            model_class=Label, template=self.prompt_template, labels=self.labels
        ).prompt.text

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_str}"},
                        },
                    ],
                }
            ],
            "max_tokens": 1000,
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        )

        response_json = response.json()["choices"][0]["message"]["content"]
        json_str = response_json.split("```json\n")[1].split("\n```")[0]
        json_data = json.loads(json_str)

        return json_data
