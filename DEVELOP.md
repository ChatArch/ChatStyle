# Development Guide

## Goal

This repository extracts reusable CLI interaction logic from ChatTool.

Current rule:

- copy logic here first
- make it reusable here
- only later decide whether ChatTool should depend on it directly

## Scope

Keep only generic and reusable pieces here:

- interactive mode policy
- missing-argument behavior
- secret masking
- lightweight prompt/runtime helpers

Do not move product-specific business logic here.
