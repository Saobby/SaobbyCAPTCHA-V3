from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
import os
from config import BACKGROUND_IMAGES_DIR, FONTS_DIR, WORDS_PATH, TIP_FONT_SIZE, TIP_MAX_ROTATE_ANGLE, CHALLENGE_MAX_ROTATE_ANGLE, CHALLENGE_FONT_SIZE, DO_INIT
from util import check_pos

bg_image_paths = []
font_paths = []
words = []


def init() -> None:
    """
    初始化所有背景图片的路径、字体路径，加载词语
    :return: None
    """
    global words
    for a, b, c in os.walk(BACKGROUND_IMAGES_DIR):
        for d in c:
            if d.endswith(".preprocessed.jpg"):
                path = (a + "/" + d).replace("\\", "/")
                bg_image_paths.append(path)
    for a, b, c in os.walk(FONTS_DIR):
        for d in c:
            path = (a + "/" + d).replace("\\", "/")
            font_paths.append(path)
    with open(WORDS_PATH, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")
    words = [line for line in lines if 2 <= len(line) <= 5 and line not in words]  # 实测使用列表推导式比使用循环append快**很多**，尤其是在你有几万个词时


def preprocess_bg_images() -> None:
    """
    预处理背景图片，全部缩放为 300px*225px ，并保存为 jpeg 格式
    :return: None
    """
    for a, b, c in os.walk(BACKGROUND_IMAGES_DIR):
        for d in c:
            if not d.endswith(".preprocessed.jpg"):
                path = (a + "/" + d).replace("\\", "/")
                img = Image.open(path)
                img = img.convert("RGB").resize((300, 225))
                img.save(path+".preprocessed.jpg", format="jpeg")
                os.remove(path)
                print(f"成功预处理了 {d}")


def gen_random_color() -> tuple:
    """
    生成一个随机的不太淡的字体颜色
    :return: tuple(R, G, B, A)
    """
    return random.randint(50, 200), random.randint(50, 200), random.randint(50, 200), 255


def gen_challenge() -> tuple[str, list[tuple[str, int, int]], bytes, bytes]:
    """
    生成一个完整的验证码
    :return: 一个 tuple
        第一项是一个 str ,为正确的词汇
        第二项是一个 list，里面包含按顺序的词汇中每个字的坐标
            格式是 ["字", x, y]
        第三项是一个 bytes，是提示图片的数据
        第四项是一个 bytes，是验证码图片的数据
    """
    bg_img = Image.open(random.choice(bg_image_paths))
    word = random.choice(words)
    chr_pos = []  # 格式: [("字", x, y), ("字", x, y)]
    tip_img = Image.new("RGBA", (int(TIP_FONT_SIZE*1.2*len(word)), int(TIP_FONT_SIZE*1.4)), (255, 255, 255, 0))
    count = 0
    for character in word:
        challenge_chr_img = Image.new("RGBA", (int(CHALLENGE_FONT_SIZE * 1.2), int(CHALLENGE_FONT_SIZE * 1.2)), (255, 255, 255, 0))
        tip_chr_img = Image.new("RGBA", (int(TIP_FONT_SIZE*1.2), int(TIP_FONT_SIZE*1.2)), (255, 255, 255, 0))
        cci_draw = ImageDraw.Draw(challenge_chr_img)
        tci_draw = ImageDraw.Draw(tip_chr_img)
        cci_font = ImageFont.truetype(random.choice(font_paths), size=CHALLENGE_FONT_SIZE)
        tci_font = ImageFont.truetype(random.choice(font_paths), size=TIP_FONT_SIZE)
        cci_draw.text((0, 0), character, font=cci_font, fill=gen_random_color())
        challenge_chr_img = challenge_chr_img.rotate(random.randint(-CHALLENGE_MAX_ROTATE_ANGLE, CHALLENGE_MAX_ROTATE_ANGLE), expand=True) # 旋转字
        tci_draw.text((0, 0), character, font=tci_font, fill=gen_random_color())
        tip_chr_img = tip_chr_img.rotate(random.randint(-TIP_MAX_ROTATE_ANGLE, TIP_MAX_ROTATE_ANGLE), expand=True)  # 旋转字
        while True:  # 生成一个随机的坐标，用于把字粘贴在背景上
            challenge_chr_x = random.randint(0, bg_img.size[0] - challenge_chr_img.size[0])
            challenge_chr_y = random.randint(0, bg_img.size[1] - challenge_chr_img.size[1])
            challenge_chr_centre_x = challenge_chr_x + int(challenge_chr_img.size[0] / 2)
            challenge_chr_centre_y = challenge_chr_y + int(challenge_chr_img.size[1] / 2)
            # 检查是否和前面的字重合
            if not check_pos((challenge_chr_centre_x, challenge_chr_centre_y), chr_pos, CHALLENGE_FONT_SIZE * 1.2):
                break  # 满足要求
        background_blank = Image.new("RGBA", bg_img.size, (0, 0, 0, 0))  # 空白背景
        tip_blank = Image.new("RGBA", tip_img.size, (0, 0, 0, 0))  # 空白提示图片
        background_blank.paste(challenge_chr_img, (challenge_chr_x, challenge_chr_y))  # 把一个字的图片粘贴在空白背景上
        tip_blank.paste(tip_chr_img, (int(TIP_FONT_SIZE*1.2*count), 0))  # 把一个提示字粘贴在空白提示图片上
        bg_img = Image.composite(background_blank, bg_img, background_blank)  # 把背景和贴了一个字的空白背景合成一张背景
        tip_img = Image.composite(tip_blank, tip_img, tip_blank)  # 把提示字图片和贴了一个字的空白提示图片合成一个提示图片
        # 问题: 为什么不直接把字贴在背景和提示图上，要先贴在空白图片上再把得到的图片和原本的图片合成一张图
        # 答案: 直接贴上去会把单个字图片的透明部分也贴上去，导致原图被镂空
        #       同时Image.composite又只支持两张同样大小的图合成，所以把贴图和合成图两个方法结合起来用
        chr_pos.append((character, challenge_chr_centre_x, challenge_chr_centre_y))
        count += 1
    challenge_img_io = BytesIO()
    tip_img_io = BytesIO()
    bg_img = bg_img.convert("RGB")
    tip_img = tip_img.convert("RGB")
    bg_img.save(challenge_img_io, format="jpeg")  # 转为jpg格式，省流量，然后把图片保存到内存
    tip_img.save(tip_img_io, format="jpeg")
    challenge_img_io.seek(0)
    tip_img_io.seek(0)
    return word, chr_pos, tip_img_io.read(), challenge_img_io.read()


if DO_INIT:
    preprocess_bg_images()
init()
if __name__ == "__main__":
    print(gen_challenge())
