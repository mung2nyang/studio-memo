#!/usr/bin/env python3
"""스튜디오 메모 PWA 아이콘 생성 (웜그레이 모노톤 말풍선).

512 좌표계로 설계하고 4배 슈퍼샘플링 후 LANCZOS 리샘플링해
192x192 / 512x512 PNG를 만든다. 마스커블 안전영역(중앙 80%) 안에 그림이 들어가도록
여백을 둔다.
"""
from PIL import Image, ImageDraw

S = 4                      # supersample factor
BASE = 512                 # design canvas size
CANVAS = BASE * S

BG = (247, 246, 243, 255)  # #F7F6F3
INK = (31, 31, 31, 255)    # #1F1F1F


def sc(*vals):
    return [v * S for v in vals]


def draw_icon() -> Image.Image:
    img = Image.new("RGBA", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)

    # 말풍선 몸통 (둥근 사각형)
    bx0, by0, bx1, by1, br = 120, 128, 392, 344, 52
    d.rounded_rectangle(sc(bx0, by0, bx1, by1), radius=br * S, fill=INK)

    # 꼬리 (왼쪽 아래로 뾰족하게) — 몸통과 겹쳐 이음새 없이 붙인다
    d.polygon([(176 * S, 330 * S), (176 * S, 398 * S), (250 * S, 330 * S)], fill=INK)

    # 안쪽 텍스트 라인 2줄
    for x0, x1, y0, y1 in ((154, 288, 195, 217), (154, 338, 255, 277)):
        d.rounded_rectangle(sc(x0, y0, x1, y1), radius=11 * S, fill=BG)

    return img


def save(img: Image.Image, size: int, path: str) -> None:
    out = img.resize((size, size), Image.LANCZOS)
    out.save(path, format="PNG", optimize=True)
    print(f"{path}  {out.size[0]}x{out.size[1]}  mode={out.mode}")


if __name__ == "__main__":
    icon = draw_icon()
    save(icon, 512, "icon-512.png")
    save(icon, 192, "icon-192.png")
