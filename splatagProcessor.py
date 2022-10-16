import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

cur_path = os.getcwd()
badge_folder = os.path.join(cur_path, 'resources', 'badge')
background_folder = os.path.join(cur_path, 'resources', 'background')
title_folder = os.path.join(cur_path, 'resources', 'title')
en_font_path = os.path.join(cur_path, 'resources', 'font', 'SplatoonFontFix.otf')
cn_font_path = os.path.join(cur_path, 'resources', 'font', 'WenYue_XinQingNianTi_J-W8.otf')


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


def add_badge(back, badge_list, badge_pos):
    for i in range(len(badge_list)):
        if badge_list[i] != "":
            back.paste(badge_list[i], badge_pos[i], badge_list[i])
        else:
            continue

    return back


def add_text(drawer, text, text_pos, font):
    drawer.text(xy=text_pos,
                text=text,
                fill="#FFFFFF",
                font=font,
                anchor="lt")

    return drawer


def get_tag_img(player_name, back_name, badge_name, title, mode, id):
    back = circle_corner(get_tag_background(back_name), 6)
    back_width = back.size[0]
    back_height = back.size[1]
    width_offset = int(back_width * 0.01)
    height_offset = int(back_height * 0.06)

    badge_size = (65, 65)
    badge_list = []
    badge_pos = []
    for i in range(len(badge_name)):
        if badge_name[i] != "":
            badge_list.append(get_tag_badge(badge_name[i]).resize(badge_size, Image.ANTIALIAS))
        else:
            badge_list.append("")
        seq = 3 - i
        pos = (back_width - seq * badge_size[0] - seq * width_offset,
               back_height - badge_size[0] - height_offset)
        badge_pos.append(pos)
    add_badge(back, badge_list, badge_pos)

    player_name_size = 75
    title_size = 32
    id_size = 25

    player_name_ttf = ImageFont.truetype(en_font_path, player_name_size)
    id_ttf = ImageFont.truetype(en_font_path, id_size)
    if mode == "cn":
        title_ttf = ImageFont.truetype(cn_font_path, title_size)
    else:
        title_ttf = ImageFont.truetype(en_font_path, title_size)

    drawer = ImageDraw.Draw(back)

    _, _, player_name_width, player_name_height = drawer.textbbox((0, 0), player_name, player_name_ttf, anchor="lt")
    _, _, title_width, title_height = drawer.textbbox((0, 0), title, title_ttf, anchor="lt")
    _, _, id_width, id_height = drawer.textbbox((0, 0), id, id_ttf, anchor="lt")

    player_name_pos = (0.5 * (back_width - player_name_width), 0.5 * (back_height - player_name_height))
    title_pos = (0 + width_offset, 0 + height_offset)
    id_pos = (0 + width_offset, back_height - id_height - height_offset)

    add_text(drawer, player_name, player_name_pos, player_name_ttf)
    add_text(drawer, title, title_pos, title_ttf)
    add_text(drawer, id, id_pos, id_ttf)

    return back


if __name__ == '__main__':
    # 输入用户名
    player_name = "I_love_Missiles"
    # 输入背景文件名，背景资源位于resources/background中
    back_name = "Npl_Catalog_Season01_Lv31.webp"
    # 输入徽章文件名，徽章资源位于resources/badge，不需要可置为“”
    badge_name = ["Badge_WinCount_WeaponSp_SpMultiMissile_Lv00.webp",
                  "Badge_WinCount_WeaponSp_SpMultiMissile_Lv01.webp",
                  "Badge_WinCount_WeaponSp_SpMultiMissile_Lv02.webp"]
    # 输入称号，称号格式形容词（adjectives）+ 对象（subjects），所有称号位于resources/title
    title = "心跳加速的多重导弹操作者"
    # 输入id
    id = "#2101"

    # 若称号为中文，则mode="cn"以匹配合适的字体文件
    img = get_tag_img(player_name, back_name, badge_name, title, "cn", id)
    img.show()
