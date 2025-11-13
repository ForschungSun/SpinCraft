BACKGROUND_COLOR = "#1f2430"
OUTER_RING_COLOR = "#4c566a"
CENTER_DOT_COLOR = "#d8dee9"
POINTER_COLOR = "#ebcb8b"

# a soft, cool palette
SECTOR_COLORS = [
    "#A4D4F5",  # 1. 浅蓝
    "#B5E4E0",  # 2. 浅青
    "#B6E8B0",  # 3. 浅绿
    "#F8E8A0",  # 5. 浅黄
    "#F3CFA4",  # 6. 浅橙
    "#F5B4C4",  # 7. 浅粉
    "#C7B5F5",  # 8. 浅紫
]


def get_sector_color(index: int) -> str:
    return SECTOR_COLORS[index % len(SECTOR_COLORS)]
