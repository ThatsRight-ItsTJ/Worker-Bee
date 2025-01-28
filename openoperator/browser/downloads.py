from dataclasses import dataclass
from langchain_core.messages import HumanMessage, SystemMessage
import os
import tarfile
from typing import List
from PIL import Image
import io
import base64
import fitz

class DownloadsRegistry:
    def __init__(self):
        self.items: list[DownloadedItem] = []

    @property
    def state(self) -> str:
        return self.current_directory()

    def current_directory(self) -> str:
        directory = []
        for item in self.items:
            if item._extracted:
                continue
            directory_record = item.fullpath
            if item._accessed:
                directory_record += " <-- THIS FILE HAS ALREADY BEEN ACCESSED BY YOU"
            directory.append(directory_record)
        return "\n".join(directory)
    
    def open_file(self, path: str) -> HumanMessage | SystemMessage:
        for item in self.items:
            if item.fullpath == path:
                item._accessed = True
                return item.content
        return SystemMessage(content=f"File not found: {path}")

    def register_file(self, item: 'DownloadedItem') -> None:
        self.items.append(item)
        

class DownloadedItem:
    def __init__(self, 
                 path: str, 
                 registry: DownloadsRegistry):
        self.fullpath = path
        self.path = os.path.dirname(path)
        self.name = os.path.basename(path)
        self.type = os.path.splitext(self.name)[1]
        self.registry = registry
        
        # Register this item immediately after initialization
        self.registry.register_file(self)

        self._content = None
        self._accessed = False
        self._extracted = False
        self._notification_sent = False

        # Process based on file type - we trust the extension since it's set based on content-type
        if self.type == '.pdf':
            self._content = self._pdf_to_message()
            
        elif self.type in ['.gz', '.tgz']:
            self._extract_targz()
            self._extracted = True
            # Process extracted files recursively
            extract_path = f"{self.fullpath}_extracted"
            for root, _, files in os.walk(extract_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    DownloadedItem(full_path, self.registry)  # These will also register themselves

        # TODO: add handlers for other file types
    
    @property
    def content(self) -> HumanMessage | SystemMessage:
        if self._content is None:
            return SystemMessage(content="Failed to open the file.")
        self._accessed = True
        return self._content

    def _extract_targz(self) -> None:
        extract_path = f"{self.fullpath}_extracted"
        os.makedirs(extract_path, exist_ok=True)

        with tarfile.open(self.fullpath, "r:gz") as tar:
            tar.extractall(path=extract_path)

    def _pdf_to_message(self) -> HumanMessage | SystemMessage:
        try:
            pdf_document = fitz.open(self.fullpath) # type: ignore

        except Exception:
            return SystemMessage(content="Failed to open the file.")
            
        message = [
            {
				"type": "text",
				"text": "You just opened a PDF file. Here are the pages: "
			}
        ]
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap() # type: ignore
            img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples) # type: ignore
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            base64_string = base64.b64encode(buffer.getvalue()).decode()
            message.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_string}"},
                } #type: ignore
            )
        pdf_document.close()

        message = HumanMessage(content=message, additional_kwargs={"label": "file_content"}) #type: ignore

        return message
    

