# Creating a Pull Request for Wyrdcraft Paintings - For Dummies

So, you've added a custom painting for Wyrdcraft and need to get it into the datapack.

Don't panic.

You **do not need to be a programmer**, and you don't need to understand all the weird Git terminology. This guide will walk you through the process using **GitHub Desktop**, step by step.

We'll be working with the Wyrdcraft Custom Paintings repository:
[**WyrdcraftOnline/wyrd-paintings**](https://github.com/WyrdcraftOnline/wyrd-paintings)

---
# First: What Even Is a Pull Request?

Think of the repository as the **official copy** of the Wyrdcraft custom paintings datapack.

Instead of editing that official copy directly, you:
1. Make your own temporary copy of the work called a **branch**.
2. Add your painting files to that branch.
3. Save your changes with a **commit**.
4. Upload your branch to GitHub with a **push**.
5. Ask Wyrdcraft to add your changes to the official version with a **Pull Request**, usually shortened to **PR**.

In other words:
> [!NOTE]
> **Branch -> Make Changes -> Commit -> Push -> Pull Request -> Review -> Merge**

Once the PR is approved and merged, your changes become part of the main Wyrdcraft custom paintings datapack.

---
# Before You Start

You'll need:
* [ ] A GitHub account
* [ ] [GitHub Desktop](https://desktop.github.com/download/) installed
* [ ] Access to the [`WyrdcraftOnline/wyrd-paintings`](https://github.com/WyrdcraftOnline/wyrd-paintings) repository
* [ ] Permission for Wyrdcraft to use the artwork
* [ ] Your painting title, author name, width, and height
* [ ] A lowercase painting asset ID
* [ ] Matching resource-pack assets in the [`WyrdcraftOnline/custom-models`](https://github.com/WyrdcraftOnline/custom-models) repository
* [ ] A painting that you've tested in Minecraft

The painting datapack and the custom models resource pack work together. This repository registers the painting in Minecraft. The custom models repository provides the painting texture, item icon, model entry, and display name.

---
# Part 1 - Download the Repository

You only have to do this the **first time** you work with the repository.

## Step 1: Open GitHub Desktop

Open **GitHub Desktop**.

> [!NOTE]
> If this is your first time using it, sign in using your GitHub account.

---
## Step 2: Clone the Wyrdcraft Repository

1. In GitHub Desktop: **File -> Clone Repository**
2. Select `WyrdcraftOnline/wyrd-paintings`. GitHub Desktop will ask where you want to save the repository on your computer. The default location is usually fine.
3. Click **Clone**. GitHub Desktop will download the datapack onto your computer.

### Congratulations.

You have successfully done a Git Thing.

---
# Part 2 - Make Sure You Have the Latest Version

Before adding anything, make sure your copy of the datapack is up to date.

> [!IMPORTANT]
> Do this every time before starting new work.
> It helps prevent your changes from colliding with someone else's.

1. At the top of GitHub Desktop, make sure your branch says: `main`
2. Then click: **Fetch origin**. If GitHub Desktop changes the button to **Pull origin**, click that too.

This downloads any changes that other Wyrdcraft members have made since the last time you updated your copy.

---
# Part 3 - Create Your Branch

> [!IMPORTANT]
> **DO NOT make your changes directly on `main`.**

The Wyrdcraft repository expects contributors to commit their work to a new branch before opening a Pull Request.

1. At the top of GitHub Desktop, click **Current Branch**
2. Then click **New Branch**
3. Give your branch a short name describing what you're adding

> [!NOTE]
> Try to use:
> * Lowercase letters
> * Hyphens instead of spaces
> * A short description of what you're changing
>
> For example:
> `sho/cottage-sunset-painting`
>
> or:
> `lewis/spawn-map-painting`
>
> or:
> `dadmann/fresh-start-painting`

4. Then click **Create Branch**

GitHub Desktop should now show your new branch instead of `main`.

---
# Part 4 - Add Your Custom Painting

Now you can edit the datapack like any other folder on your computer.

The easiest way is to use the helper script:

```sh
make painting
```

On Windows, if `make painting` does not work, open **PowerShell** in the repository folder and run:

```powershell
py scripts\create_painting.py
```

If that does not work but Python is installed, try:

```powershell
python scripts\create_painting.py
```

The script asks for:
* Painting asset ID
* Width
* Height
* Title
* Author

It automatically creates the painting variant JSON, creates the recipe JSON, adds the next available `/trigger painting` value, and updates the Current Paintings section of `README.md`.

> [!NOTE]
> If the automatic script doesn't work for you, you can either reach out to someone else for help or add files manually.
> If you choose to create the files manually, continue reading. Manual file creation is covered later.

> [!IMPORTANT]
> The asset ID must exactly match the painting asset ID used in the custom models resource pack.

---
# Part 5 - Choose a Safe Painting ID

Painting IDs should contain:
* Lowercase letters
* Numbers if needed
* Underscores

Avoid:
* Spaces
* Capital letters
* Hyphens
* Special characters

> [!NOTE]
> Good IDs:
> `dadmannwalking01`
> `wyrd_spawn_map`
> `sho_cottage_sunset`

> [!NOTE]
> Bad IDs:
> `DadmannWalking01`
> `wyrd-spawn-map`
> `Sho Cottage Sunset!`

Minecraft is particularly picky about resource locations, so boring IDs are good IDs.

---
# Part 6 - Know What Files Are Created

If you run `make painting`, the script handles this for you. Still, it helps to know what should change.

The painting variant goes here:

```text
season_one/data/wyrd_painting/painting_variant/
```

The recipe goes here:

```text
season_one/data/wyrd_painting/recipe/painting_variant/
```

The trigger helper is here:

```text
season_one/data/wyrd_painting/function/trigger.mcfunction
```

The Current Paintings list is in:

```text
README.md
```

## If the Script Does Not Work

You can add the painting manually. Use your **real painting ID** everywhere this example says `your_painting_id`.

### 1. Create the Painting Variant

Create a new file here:

```text
season_one/data/wyrd_painting/painting_variant/your_painting_id.json
```

Put this inside it:

```json
{
  "asset_id": "wyrd_painting:your_painting_id",
  "width": 2,
  "height": 1,
  "title": {
    "text": "Your Painting Title",
    "color": "yellow"
  },
  "author": {
    "text": "YourName",
    "color": "gray"
  }
}
```

Change `width`, `height`, `title`, and `author` to match your painting.

### 2. Create the Recipe

Create a matching file here:

```text
season_one/data/wyrd_painting/recipe/painting_variant/your_painting_id.json
```

Put this inside it:

```json
{
  "type": "minecraft:stonecutting",
  "ingredient": "minecraft:painting",
  "result": {
    "components": {
      "minecraft:painting/variant": "wyrd_painting:your_painting_id"
    },
    "count": 1,
    "id": "minecraft:painting"
  }
}
```

### 3. Add Trigger Access

Open this file:

```text
season_one/data/wyrd_painting/function/trigger.mcfunction
```

Look for the highest existing `painting=` number, then add the next number on a new line.

For example, if the highest existing number is `3`, add your painting as `4`:

```mcfunction
execute as @a[scores={painting=4}] at @s run give @s minecraft:painting[ minecraft:painting/variant="wyrd_painting:your_painting_id" ]
```

> [!IMPORTANT]
> Do not reuse a trigger number that already exists.
> One trigger number should give one painting.

### 4. Update the README

Open `README.md`, find the **Current Paintings** section, and add your painting to the list:

```markdown
- `your_painting_id`: Your Painting Title, 2x1, by YourName
```

Use the same width, height, title, and author that you used in the painting variant JSON.

> [!IMPORTANT]
> If GitHub Desktop shows generated release zip files under `releases/`, do not include those in an ordinary painting PR unless a maintainer specifically asked for them.

---
# Part 7 - Add the Resource Pack Assets

This paintings repository only handles the datapack side.

You also need matching resource-pack files in:
[**WyrdcraftOnline/custom-models**](https://github.com/WyrdcraftOnline/custom-models)

In the custom models repository, run:

```sh
make painting
```

On Windows, if `make painting` does not work, open **PowerShell** in the custom models repository folder and run:

```powershell
py scripts\create_painting.py
```

If that does not work but Python is installed, try:

```powershell
python scripts\create_painting.py
```

Use the exact same painting asset ID.

The custom models repository adds the painting art, item icon mapping, model entry, and display name. See that repository's custom painting guide for the asset-side steps:
[custom_paintings.md](https://github.com/WyrdcraftOnline/custom-models/blob/main/custom_paintings.md)

> [!NOTE]
> If your painting needs both repositories changed, you will usually open one PR in `wyrd-paintings` and one matching PR in `custom-models`.

---
# Part 8 - Test Your Painting

Before submitting your PR, test the datapack and resource pack in Minecraft.

Make sure:
* [ ] The datapack loads
* [ ] The resource pack loads
* [ ] The painting appears in game
* [ ] The painting has the correct width and height
* [ ] The title and author look right
* [ ] The `/trigger painting` helper gives the correct painting
* [ ] The texture appears correctly
* [ ] You haven't accidentally changed someone else's painting
* [ ] Minecraft doesn't complain about broken JSON or missing files

For example, if your painting was assigned trigger value `3`, you would test it with:

```mcfunction
/trigger painting set 3
```

Do **not** submit something you've never tested.

---
# Part 9 - Commit Your Changes

1. Go back to GitHub Desktop.
2. On the left side of the window, you'll see a list of everything you've changed.
3. Take a second to look through it.
4. **Make sure you recognize all of the files.**
5. If GitHub Desktop says you modified 4 files and you expected to modify 4 files, great. If GitHub Desktop says you modified 327 files, something has probably gone wrong. Ask someone before continuing.
6. At the bottom-left of GitHub Desktop you'll see **Summary (required)**. This is your commit message. Write a short description of what you added. You generally don't need anything in the larger Description box.

> [!NOTE]
> Simple is just as good as complex. For example:
> `Add cottage sunset painting`
>
> or:
> `Add spawn map painting`
>
> or:
> `Add dadmannwalking03 painting`

7. Then click **Commit to YOUR-BRANCH-NAME**. For example: **Commit to dadmann/fresh-start-painting**

---
# Part 10 - Push Your Branch to GitHub

Your changes are currently only saved on **your computer**. Now we need to send them to GitHub.

1. At the top of GitHub Desktop, click **Publish branch**. Sometimes this may instead say **Push origin**. Click it.

Your branch now exists on GitHub.

> [!IMPORTANT]
> Another Git Thing accomplished.

---
# Part 11 - Create the Pull Request

1. After publishing your branch, GitHub Desktop will usually display a button that says **Create Pull Request**. Click it.
2. GitHub Desktop will open GitHub in your browser. You should see something similar to **base: main <- compare: your-branch-name**

> [!IMPORTANT]
> The **base** should be:
> `main`
>
> The **compare** branch should be the branch you just created.
> You are asking GitHub:
>
> "Please take the changes from my branch and add them to `main`."

---
# Part 12 - Give Your PR a Name

Give your Pull Request a short, useful title.

> [!NOTE]
> Good PR names:
> * `Add Cottage Sunset painting`
> * `Add dadmannwalking03 painting`
> * `Add Spawn Map custom painting`

> [!NOTE]
> Not so good PR names:
> * `stuff`
> * `changes`
> * `please merge`
> * `idk github told me to type something here`

---
# Part 13 - Describe What You Changed

GitHub will show the repository's PR template. Fill it out so the reviewer can understand what changed.

For example:

```markdown
## Summary

Added the Cottage Sunset custom painting.

## Paintings

- `sho_cottage_sunset`: Cottage Sunset, 2 x 1, by SHO310

## Checklist

* [x] Wyrdcraft has permission to use the artwork
* [x] Painting IDs use lowercase letters, numbers, and underscores only
* [x] Painting variant JSON was added or updated
* [x] Recipe JSON was added or updated
* [x] Trigger access was updated, if needed
* [x] Matching resource pack assets were added or updated in the custom models repo
* [x] The README Current Paintings section was updated
* [x] The painting was tested in game, or testing notes are included below
* [x] Generated release zips were not included in this PR

## Testing Notes

Tested in game with `/trigger painting set 3`.

## Resource Pack PR

https://github.com/WyrdcraftOnline/custom-models/pull/123
```

It doesn't need to be an essay.

The goal is just to make it easy for the reviewer to understand what you've changed.

---
# Part 14 - Create the Pull Request

1. Click **Create Pull Request**
2. And that's it.

> [!IMPORTANT]
> Seriously.
> You're done.
> You have successfully created a Pull Request.

---
# What Happens Now?

Another Wyrdcraft collaborator will review your changes. They might:
1. **Approve it**. Everything looks good.
2. **Leave a comment**. They have a question.
3. **Request changes**. Something needs to be fixed before the painting is added.

Don't panic if someone requests changes.

That's literally what Pull Requests are for.

The Wyrdcraft repository requires changes to be reviewed before they're merged into `main`.

---
# "Someone Asked Me to Change Something. Now What?"

You **do not need to create another Pull Request.**

1. Go back to GitHub Desktop.
2. Make sure you're still on the same branch you used for the PR. For example: `dadmann/fresh-start-painting`
3. Make the requested changes.
4. Check the changed files in GitHub Desktop.
5. Write another commit message.
6. Click **Commit**.
7. Click **Push origin**.

That's it. GitHub automatically adds the new commit to your existing Pull Request.

---
# After Your Pull Request Is Approved

Once everything looks good, the PR can be merged into `main`.

The Wyrdcraft repository automatically handles creation of the updated datapack release after approved changes are merged, so contributors do **not** need to manually build a release.

---
# Starting Your Next Painting

When you're ready to work on something else:

1. Switch back to `main`. In GitHub Desktop, **Current Branch -> main**
2. Update it. Click **Fetch origin** and, if shown, **Pull origin**
3. Create another new branch
4. Start working

Do **not** keep reusing your old branch for unrelated paintings.

New change = new branch = new Pull Request.

---
# The Entire Process in 30 Seconds

Every time you want to submit something:
* [ ] Switch to `main`
* [ ] Fetch/Pull the latest changes
* [ ] Create a new branch
* [ ] Confirm Wyrdcraft has permission to use the artwork
* [ ] Choose a lowercase painting ID
* [ ] Run `make painting`, run `py scripts\create_painting.py` on Windows, or add the files manually
* [ ] Add the matching resource-pack assets in `custom-models`
* [ ] Test the painting in Minecraft
* [ ] Review the files GitHub says you changed
* [ ] Make sure generated release zips are not included
* [ ] Commit your changes
* [ ] Push/Publish your branch
* [ ] Create a Pull Request into `main`
* [ ] Link the matching resource-pack PR, if there is one
* [ ] Wait for review
* [ ] Make fixes on the same branch if requested

---
# Git Vocabulary for Normal Humans

**Repository / Repo**: The project folder GitHub keeps track of.

For us:
`WyrdcraftOnline/wyrd-paintings`

---

**main**: The official/current version of the project.

Try not to directly mess with it.

---

**Branch**: Your temporary workspace.

You make changes here without changing the official version.

Example:
`dadmann/fresh-start-painting`

---

**Commit**: A saved checkpoint containing your changes.

Example:
`Add fresh start painting`

---

**Push**: Uploads your commits from your computer to GitHub.

---

**Pull**: Downloads newer changes from GitHub to your computer.

---

**Fetch**: Checks GitHub to see whether newer changes exist.

---

**Pull Request / PR**: A request asking:
> "Can we add the changes from my branch to `main`?"

---

**Review**: Another person checks your changes before they become official.

---

**Merge**: The Pull Request was approved and your branch's changes were added to `main`.

---
# Something Looks Wrong?

If any of these happen:
* GitHub says there are conflicts
* Hundreds of unexpected files have changed
* You accidentally worked directly on `main`
* You used the wrong painting ID
* You're not sure which dimensions to use
* You're not sure whether Wyrdcraft has permission to use the artwork
* You're not sure which folder a file belongs in
* Your branch won't push
* Your Pull Request won't merge
* GitHub starts yelling words at you that aren't covered in this document

**Stop and ask in the Wyrdcraft Discord.**

You are significantly less likely to break anything by asking before clicking random buttons.

And even if you do mess something up:

That's one of the reasons we're using Git in the first place.

Usually, it's fixable.
