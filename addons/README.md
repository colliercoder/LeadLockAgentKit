# Add-ons

This folder is where paid Leadlock add-ons go. Everything you drop in here stays on your
machine: the whole folder (except this file) is in `.gitignore`, so it never gets pushed to
GitHub or shared.

## Leadlock Launch Bundle

The Launch Bundle adds GoHighLevel superpowers to the kit:

- **GHL CLI and Claude skill**: Claude can read and change your GoHighLevel account from
  the terminal (contacts, opportunities, calendars, workflows, conversations and more).
- **Leadlock GHL Connector**: a small Chrome extension that copies your own GoHighLevel
  login token, so Claude can build and update workflows for you.

Get it at https://www.leadlock.ai/store

## Install an add-on

1. Unzip what you got after purchase into this folder, so you have
   `addons/leadlock-launch-bundle/`.
2. Open Claude Code in the kit folder and say: **"install my add-on"**.

Claude runs the `install-addon` skill: it installs the add-on, connects its Claude skill to
the kit, reuses the GoHighLevel keys already in your `.env`, and walks you through loading
the Chrome extension.
