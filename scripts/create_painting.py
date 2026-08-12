#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


NAMESPACE = "wyrd_painting"
VALID_ASSET_ID = re.compile(r"^[a-z0-9_]+$")
TRIGGER_SCORE = re.compile(r"scores=\{painting=(\d+)\}")


def prompt(label, validator=None):
    while True:
        value = input(f"{label}: ").strip()
        if not value:
            print("Value is required.")
            continue
        if validator:
            error = validator(value)
            if error:
                print(error)
                continue
        return value


def validate_asset_id(value):
    if ":" in value:
        return "Enter only the asset ID, without the namespace. Example: dadmannwalking01"
    if not VALID_ASSET_ID.match(value):
        return "Use only lowercase letters, numbers, and underscores."
    return None


def validate_int(value):
    try:
        number = int(value)
    except ValueError:
        return "Enter a whole number."
    if number < 1:
        return "Enter a number greater than 0."
    return None


def confirm_overwrite(paths):
    existing = [path for path in paths if path.exists()]
    if not existing:
        return True

    print("\nThe following files already exist:")
    for path in existing:
        print(f"- {path}")

    try:
        answer = input("Overwrite them? [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def get_next_trigger_value(trigger_path):
    if not trigger_path.exists():
        return 1

    values = [
        int(match.group(1))
        for match in TRIGGER_SCORE.finditer(trigger_path.read_text(encoding="utf-8"))
    ]
    return max(values, default=0) + 1


def update_trigger_function(trigger_path, trigger_value, namespaced_id):
    trigger_path.parent.mkdir(parents=True, exist_ok=True)
    if trigger_path.exists():
        content = trigger_path.read_text(encoding="utf-8")
    else:
        content = (
            "#\n"
            "# Description:\tgive commands for trigger\n"
            "# Called by:\twyrd_painting:second\n"
            "# Entity @s:\tplayer\n"
            "#\n"
        )

    if namespaced_id in content:
        return False

    line = (
        f'execute as @a[scores={{painting={trigger_value}}}] at @s run give @s '
        f'minecraft:painting[ minecraft:painting/variant="{namespaced_id}" ]'
    )
    if content and not content.endswith("\n"):
        content += "\n"
    content += line + "\n"
    trigger_path.write_text(content, encoding="utf-8")
    return True


def update_readme(readme_path, asset_id, title, width, height, author):
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")
    entry = f"- `{asset_id}`: {title}, {width}x{height}, by {author}"
    if f"- `{asset_id}`:" in content:
        return False

    heading = "## Current Paintings"
    heading_index = content.find(heading)
    if heading_index == -1:
        return False

    first_fence = content.find("```", heading_index)
    if first_fence == -1:
        return False

    first_fence_end = content.find("\n", first_fence)
    if first_fence_end == -1:
        return False

    closing_fence = content.find("```", first_fence_end + 1)
    if closing_fence == -1:
        return False

    insertion = entry + "\n"
    updated = content[:closing_fence] + insertion + content[closing_fence:]
    readme_path.write_text(updated, encoding="utf-8")
    return True


def main():
    repo_root = Path(__file__).resolve().parents[1]
    season_file = repo_root / "season.txt"

    if not season_file.exists():
        print("season.txt does not exist.", file=sys.stderr)
        return 1

    season = season_file.read_text(encoding="utf-8").strip()
    if not season:
        print("season.txt is empty.", file=sys.stderr)
        return 1

    season_dir = repo_root / season
    if not season_dir.exists():
        print(f"Season directory does not exist: {season_dir}", file=sys.stderr)
        return 1

    print("Create a Wyrdcraft custom painting datapack entry\n")
    asset_id = prompt("Asset ID", validate_asset_id)
    print("This ID must exactly match the custom models resource-pack painting asset ID.")
    width = int(prompt("Width in blocks", validate_int))
    height = int(prompt("Height in blocks", validate_int))
    title = prompt("Title")
    author = prompt("Author")

    namespaced_id = f"{NAMESPACE}:{asset_id}"
    variant_path = season_dir / "data" / NAMESPACE / "painting_variant" / f"{asset_id}.json"
    recipe_path = season_dir / "data" / NAMESPACE / "recipe" / "painting_variant" / f"{asset_id}.json"
    trigger_path = season_dir / "data" / NAMESPACE / "function" / "trigger.mcfunction"
    readme_path = repo_root / "README.md"
    trigger_value = get_next_trigger_value(trigger_path)

    if not confirm_overwrite([variant_path, recipe_path]):
        print("No files were changed.")
        return 1

    variant = {
        "asset_id": namespaced_id,
        "width": width,
        "height": height,
        "title": {
            "text": title,
            "color": "yellow",
        },
        "author": {
            "text": author,
            "color": "gray",
        },
    }

    recipe = {
        "type": "minecraft:stonecutting",
        "ingredient": "minecraft:painting",
        "result": {
            "components": {
                "minecraft:painting/variant": namespaced_id,
            },
            "count": 1,
            "id": "minecraft:painting",
        },
    }

    write_json(variant_path, variant)
    write_json(recipe_path, recipe)
    trigger_updated = update_trigger_function(trigger_path, trigger_value, namespaced_id)
    readme_updated = update_readme(readme_path, asset_id, title, width, height, author)

    print("\nCreated datapack files:")
    print(f"- {variant_path.relative_to(repo_root)}")
    print(f"- {recipe_path.relative_to(repo_root)}")
    if trigger_updated:
        print(f"- {trigger_path.relative_to(repo_root)} using /trigger painting set {trigger_value}")
    else:
        print(f"- {trigger_path.relative_to(repo_root)} already referenced {namespaced_id}")
    if readme_updated:
        print(f"- {readme_path.relative_to(repo_root)}")
    else:
        print(f"- {readme_path.relative_to(repo_root)} was not updated")

    print("\nResource-pack follow-up:")
    print(f"- Run `make painting` in the custom models repo using asset ID `{asset_id}`.")
    print(f"- The resource-pack painting asset must map to {namespaced_id}.")
    print("- See https://github.com/WyrdcraftOnline/custom-models/blob/main/custom_paintings.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
