#!/bin/bash
set -euo pipefail

TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")
SEASON=$(tr -d '[:space:]' < season.txt)
SEASON_DIR="./$SEASON"
RELEASES_DIR="./releases"
SOFT_RELEASE_ZIP="$RELEASES_DIR/$TIMESTAMP.zip"
FINAL_RELEASE_DIR="./releases/final"
FINAL_RELEASE_ZIP="$FINAL_RELEASE_DIR/release.zip"

if [ -z "$SEASON" ]; then
    echo "season.txt is empty."
    exit 1
fi

if [ ! -d "$SEASON_DIR" ]; then
    echo "Expected season datapack at $SEASON_DIR, but that directory does not exist."
    exit 1
fi

if [ ! -f "$SEASON_DIR/pack.mcmeta" ]; then
    echo "Expected pack metadata at $SEASON_DIR/pack.mcmeta, but that file does not exist."
    exit 1
fi

if [ ! -d "$SEASON_DIR/data" ]; then
    echo "Expected datapack data at $SEASON_DIR/data, but that directory does not exist."
    exit 1
fi

mkdir -p "$RELEASES_DIR" "$FINAL_RELEASE_DIR"

echo "Compressing current datapack..."
rm -f "$SOFT_RELEASE_ZIP"
(
    cd "$SEASON_DIR"
    zip -r "../$SOFT_RELEASE_ZIP" pack.mcmeta data/ -x "*.DS_Store" -x "releases/*"
)

echo "Creating final release..."
rm -f "$FINAL_RELEASE_ZIP"
cp "$SOFT_RELEASE_ZIP" "$FINAL_RELEASE_ZIP"

if [ -f "./README.md" ]; then
    echo "Copying README.md to release..."
    cp "./README.md" "$FINAL_RELEASE_DIR/README.md"
fi

printf "\e[1;31mThe soft release has been generated at %s.\e[0m\n" "$SOFT_RELEASE_ZIP"
printf "\e[1;31mA final release has been generated at %s.\e[0m\n" "$FINAL_RELEASE_ZIP"
