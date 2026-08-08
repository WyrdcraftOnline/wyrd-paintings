# Wyrdcraft Custom Paintings

This repository contains the custom paintings datapack for the Wyrdcraft SMP.

The datapack defines the custom painting variants, recipes, and trigger functions that make paintings available in game. The matching textures, item models, and language entries live in the Wyrdcraft custom models resource pack.

## How Custom Paintings Work

Custom paintings need two parts:

* A datapack entry in this repository that registers the painting variant and makes it obtainable.
* A resource pack entry in the custom models pack that provides the painting texture, item texture, model, and display name.

The datapack is responsible for Minecraft data such as:

```text
season_one/data/wyrd_painting/painting_variant/
season_one/data/wyrd_painting/recipe/painting_variant/
season_one/data/wyrd_painting/function/
```

The resource pack is responsible for assets such as:

```text
custom-models/season_one/assets/wyrd_painting/textures/painting/
custom-models/season_one/assets/wyrd_painting/textures/item/
custom-models/season_one/assets/wyrd_painting/models/item/
custom-models/season_one/assets/wyrd_painting/lang/en_us.json
custom-models/season_one/assets/minecraft/items/painting.json
```

## Repository Layout

The active season is selected by `season.txt`.

Current layout:

```text
season.txt
season_one/
  pack.mcmeta
  data/
    minecraft/
      tags/
        function/load.json
        painting_variant/placeable.json
    wyrd_painting/
      function/
      painting_variant/
      recipe/painting_variant/
```

The generated release files are written to:

```text
releases/
releases/final/
```


> [!IMPORTANT]
> Please do not include generated release zips in ordinary feature commits unless the release workflow specifically requires it.

## Adding a Custom Painting

Before adding a painting, make sure Wyrdcraft has permission to use the image.

### 1. Choose an ID

Use a lowercase, underscore-safe ID. Keep it specific enough to avoid collisions.

Good examples:

```text
dadmannwalking01
wyrd_spawn_map
sho_cottage_sunset
```

Avoid spaces, uppercase letters, hyphens, and special characters.

### 2. Add the Painting Variant

Create a JSON file in:

```text
season_one/data/wyrd_painting/painting_variant/
```

Example:

```json
{
  "asset_id": "wyrd_painting:dadmannwalking01",
  "width": 4,
  "height": 3,
  "title": {
    "text": "A Fresh Start",
    "color": "yellow"
  },
  "author": {
    "text": "dadmannwalking",
    "color": "gray"
  }
}
```

`width` and `height` are measured in Minecraft painting blocks.

### 3. Add the Recipe

Create a matching recipe in:

```text
season_one/data/wyrd_painting/recipe/painting_variant/
```

Example:

```json
{
  "type": "minecraft:stonecutting",
  "ingredient": "minecraft:painting",
  "result": {
    "components": {
      "minecraft:painting/variant": "wyrd_painting:dadmannwalking01"
    },
    "count": 1,
    "id": "minecraft:painting"
  }
}
```

This allows players to turn a regular painting into the custom variant with a stonecutter.

### 4. Update Trigger Access

If the painting should be available through the `/trigger painting` helper, add a matching give command to:

```text
season_one/data/wyrd_painting/function/trigger.mcfunction
```

Example:

```mcfunction
execute as @a[scores={painting=1}] at @s run give @s minecraft:painting[ minecraft:painting/variant="wyrd_painting:dadmannwalking01" ]
```

If multiple paintings are added, coordinate trigger values before changing this file so one value does not accidentally give several paintings.

### 5. Add the Resource Pack Assets

In the [custom models resource pack](https://github.com/WyrdcraftOnline/custom-models), add the matching painting art, item icon, model, and language entry.

At minimum, check these files and folders:

```text
custom-models/season_one/assets/wyrd_painting/textures/painting/
custom-models/season_one/assets/wyrd_painting/textures/item/
custom-models/season_one/assets/wyrd_painting/models/item/
custom-models/season_one/assets/wyrd_painting/lang/en_us.json
custom-models/season_one/assets/minecraft/items/painting.json
```

The resource pack `painting.json` must map the painting variant to the correct item model.

Example:

```json
{
  "when": "wyrd_painting:dadmannwalking01",
  "model": {
    "type": "model",
    "model": "wyrd_painting:item/dadmannwalking"
  }
}
```

## Current Paintings

The following custom paintings are currently included.

```markdown
- `dadmannwalking01`: A Fresh Start, 4x3, by dadmannwalking
```

> [!IMPORTANT]
> Please update this list as you add new paintings!

## Creating a Release

At some point, you may want to make a release to test your paintings. You can do so by opening CMD or Terminal and using the following command in the project's root directory:

```sh
make
```

This creates:

```text
releases/<timestamp>.zip
releases/final/wyrd_paintings.zip
releases/final/README.md
```

The timestamped zip is a soft release that can be used for rollback. The final zip is the stable path intended for automation or server deployment.

The release zip contains the active season datapack with `pack.mcmeta` and `data/` at the archive root.

> [!IMPORTANT]
> Please do not include generated release zips in ordinary feature commits unless the release workflow specifically requires it.

## Automatic Release Upload

When changes are pushed to `main`, GitHub Actions builds the datapack and uploads:

```text
releases/final/wyrd_paintings.zip
```

The upload workflow expects these repository secrets:

```text
SFTP_HOST
SFTP_USERNAME
SFTP_PASSWORD
SFTP_REMOTE_DIR
```

`SFTP_REMOTE_DIR` should be the server directory where `wyrd_paintings.zip` needs to be placed.

Optional SFTP secret:

```text
SFTP_PORT
```

If `SFTP_PORT` is not set, the workflow uses port `22`.

If RCON is configured, the workflow will notify active players, wait 5 minutes, and then run the restart command.

Optional RCON secrets:

```text
MC_RCON_HOST
MC_RCON_PORT
MC_RCON_PASSWORD
MC_RESTART_COMMAND
```

If `MC_RESTART_COMMAND` is not set, the workflow uses `stop`. This assumes the server host or panel will automatically start the server again. If RCON is not configured or fails, the workflow sends a Discord notification instead.

Discord fallback secret:

```text
DISCORD_WEBHOOK_URL
```

## Quick Checklist

Before opening a pull request, make sure you have:

* Confirmed Wyrdcraft has permission to use the artwork
* Used a lowercase, safe painting ID
* Added the painting variant JSON
* Added the painting recipe JSON
* Updated trigger access if needed
* Added the matching resource pack assets
* Tested the painting in game
* Updated the Current Paintings section
* Left generated release zips out of normal feature commits

## Questions or Issues

If you are unsure where a file should go, which dimensions to use, or whether artwork is approved for the server, ask in the Wyrdcraft Discord before opening a pull request.
