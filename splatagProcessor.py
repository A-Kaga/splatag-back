import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

cur_path = os.getcwd()
badge_folder = os.path.join(cur_path, 'resources', 'badge')
background_folder = os.path.join(cur_path, 'resources', 'background')
title_folder = os.path.join(cur_path, 'resources', 'title')
ttf_path = os.path.join(cur_path, 'resources', 'font', 'SplatoonFontFix.otf')


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()


def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """
    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


def get_tag_background(name):
    img = Image.open(os.path.join(background_folder, name))
    return img


def get_tag_badge(name):
    img = Image.open(os.path.join(badge_folder, name))
    return img


def get_tag_img(player_name, back_name, badge_name, title, id):
    """
    background = circle_corner(get_tag_background(back_name), 20)[1]
    badge_0 = circle_corner(get_tag_badge(badge_name[0]), 16)[0].resize(badge_size, Image.ANTIALIAS)
    badge_1 = circle_corner(get_tag_badge(badge_name[1]), 16)[1].resize(badge_size, Image.ANTIALIAS)
    badge_2 = circle_corner(get_tag_badge(badge_name[2]), 16)[2].resize(badge_size, Image.ANTIALIAS)
    """

    badge_size = (80, 80)
    player_name_size = 60
    title_size = 40
    id_size = 30

    back = circle_corner(get_tag_background(back_name), 6)
    badge_0 = get_tag_badge(badge_name[0]).resize(badge_size, Image.ANTIALIAS) if badge_name[0] != "" else None
    badge_1 = get_tag_badge(badge_name[1]).resize(badge_size, Image.ANTIALIAS) if badge_name[1] != "" else None
    badge_2 = get_tag_badge(badge_name[2]).resize(badge_size, Image.ANTIALIAS) if badge_name[2] != "" else None

    back_width = back.size[0]
    back_height = back.size[1]
    badge_size = badge_0.size[0] if badge_0 is not None else None
    offset_size = int(back_height * 0.05)

    badge_0_pos = (back_width - 3 * badge_size - 3 * offset_size, back_height - badge_size - offset_size)
    badge_1_pos = (back_width - 2 * badge_size - 2 * offset_size, back_height - badge_size - offset_size)
    badge_2_pos = (back_width - badge_size - offset_size, back_height - badge_size - offset_size)

    back.paste(badge_0, badge_0_pos)
    back.paste(badge_1, badge_1_pos)
    back.paste(badge_2, badge_2_pos)

    player_name_ttf = ImageFont.truetype(ttf_path, player_name_size)
    title_ttf = ImageFont.truetype(ttf_path, title_size)
    id_ttf = ImageFont.truetype(ttf_path, id_size)

    drawer = ImageDraw.Draw(back)

    _, _, player_name_width, player_name_height = drawer.textbbox((0, 0), player_name, player_name_ttf, anchor="lt")
    _, _, title_width, title_height = drawer.textbbox((0, 0), title, title_ttf, anchor="lt")
    _, _, id_width, id_height = drawer.textbbox((0, 0), id, id_ttf, anchor="lt")

    title_pos = (0 + offset_size, 0 + offset_size)
    player_name_pos = (0.5 * (back_width - player_name_width), 0.5 * (back_height - player_name_height) - offset_size)
    id_pos = (0 + offset_size, back_height - id_height - offset_size)

    drawer.text(xy=player_name_pos,
                text=player_name,
                fill="#FFFFFF",
                font=player_name_ttf,
                anchor="lt")

    drawer.text(title_pos,
                title, "#FFFFFF", title_ttf,
                anchor="lt")
    drawer.text(id_pos,
                id, "#FFFFFF", id_ttf,
                anchor="lt")

    return back


if __name__ == '__main__':
    '''
    player_name = "player"
    back_name = "Npl_Catalog_Season01_Lv31.webp"
    badge_name = ["Badge_CoopGrade_Normal_Shakedent_Lv00.webp",
                  "Badge_CoopGrade_Normal_Shakedent_Lv00.webp",
                  "Badge_CoopGrade_Normal_Shakedent_Lv00.webp"]
    title = "I am TITLE"
    id = "#2101"

    background = get_tag_background(back_name)

    badge_size = 30
    player_name_size = 60
    title_size = 40
    id_size = 30
    offset_size = background.size[1] * 0.03

    player_name_ttf = ImageFont.truetype(ttf_path, player_name_size)
    title_ttf = ImageFont.truetype(ttf_path, title_size)
    id_ttf = ImageFont.truetype(ttf_path, id_size)

    title_pos = (0, 0)
    player_name_pos = (0.5 * (background.size[0] - player_name_ttf.getsize(player_name)[0]),
                       0.5 * (background.size[1] - player_name_ttf.getsize(player_name)[1]))
    id_pos = (0, background.size[1] - id_size)
    drawer = ImageDraw.Draw(background)
    _, _, player_name_width, player_name_height = drawer.textbbox((0, 0), player_name, player_name_ttf, anchor="lt")
    _, _, title_width, title_height = drawer.textbbox((0, 0), title, title_ttf, anchor="lt")
    _, _, id_width, id_height = drawer.textbbox((0, 0), id, id_ttf, anchor="lt")

    drawer.text(xy=(0.5 * (background.size[0] - player_name_width), 0.5 * (background.size[1] - player_name_height) - offset_size),
                text=player_name,
                fill="#FFFFFF",
                font=player_name_ttf,
                anchor="lt")

    drawer.text((0 + offset_size, 0 + offset_size),
                title, "#FFFFFF", title_ttf,
                anchor="lt")
    drawer.text((0 + offset_size, background.size[1] - id_height - offset_size),
                id, "#FFFFFF", id_ttf,
                anchor="lt")

    background.show()
    
    '''

    player_name = "VeronIKA"
    back_name = "Npl_Catalog_Season01_Lv31.webp"
    badge_name = ["Badge_CoopGrade_Normal_Shakedent_Lv00.webp",
                  "Badge_CoopGrade_Normal_Shakedent_Lv00.webp",
                  "Badge_CoopGrade_Normal_Shakedent_Lv00.webp"]
    title = "Hotlantis Part-Timer"
    id = "#2101"

    img = get_tag_img(player_name, back_name, badge_name, title, id)
    img.show()
