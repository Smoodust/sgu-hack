from pydantic import BaseModel
from typing import List

class SuspiciousLineResponse(BaseModel):
    """
    Модель ответа с подозрительными строками логов
    """
    result: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "result": [
                    "libtool-default: link: warning: library `/usr/src/tmp/NearTree-buildroot/usr/lib64/libCNearTree.la' was moved.",
                    "libtool-default: link: warning: library `/usr/src/tmp/NearTree-buildroot/usr/lib64/libCNearTree.la' was moved.",
                    "libtool-default: link: warning: library `/usr/src/tmp/NearTree-buildroot/usr/lib64/libCNearTree.la' was moved.",
                    "libtool-default: link: warning: library `/usr/src/tmp/NearTree-buildroot/usr/lib64/libCNearTree.la' was moved.",
                    "libtool-default: link: g++ -pipe -frecord-gcc-switches -Wall -g -O2 -ansi -pedantic -DCNEARTREE_SAFE_TRIANG=1 -I. ./main.cpp ./v.cpp -o bin/CPPMain  -lm"
                ]
            }
        }