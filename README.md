# Aairy - Personal AI Agent with Memory, RAG \& Automation

A production-deployed personal AI agent built on OpenClaw with multi-layer persistent memory, semantic search, and automated knowledge extraction.

## Overview

Aairy is a personal AI agent I built from scratch while learning agentic systems. What started as following a tutorial quickly became a real engineering project — deploying a multi-layer memory architecture, building a RAG pipeline, and running automated knowledge extraction on a production Azure cloud server.

The core idea: agents should write and maintain their own memory. Aairy reads her vault at every session start, updates it during work, and runs a nightly script to extract knowledge from conversation logs automatically.

## Architecture

```

Session Logs (JSONL)

↓

Wiki Builder (nightly cron)

↓

Obsidian Vault (MD files)

├── Agent-Shared/user-profile.md

├── Agent-Shared/project-state.md

└── Agent-Aairy/daily.md

↓

ChromaDB (vector database)

↓

RAG Semantic Search

```

## Features

### 4-Layer Memory System



Layer 1: Built-in context

Layer 2: AGENTS.md and SOUL.md

Layer 3: Obsidian Vault (self-updating)

Layer 4: RAG Search (semantic retrieval)



### Auto Wiki Builder



Reads daily session logs automatically

Sends to Claude API for fact extraction

Updates vault files without human involvement

Runs nightly via Windows Task Scheduler



### RAG Semantic Search



Indexes all vault markdown files into ChromaDB

Uses sentence-transformers for embeddings

Returns only relevant context



## Tech Stack

ComponentTechnologyAgent FrameworkOpenClawLanguage ModelClaude Haiku 4.5Vector DatabaseChromaDBEmbeddingssentence-transformersKnowledge BaseObsidianCloudAzure VM Ubuntu 24LanguagePython 3ChannelsTelegram

## What I Learned

### Memory Architecture

Most AI agents forget everything when a session ends. Building Aairy taught me how to solve this properly by building a real persistent memory layer that the agent owns and maintains herself.

### RAG From Scratch

Built the full RAG pipeline without LangChain. Direct ChromaDB plus sentence-transformers. Deep understanding of embeddings, cosine similarity, and metadata filtering.

### Production Deployment

Deployed on Azure server with SSH. Learned Linux cron jobs, file permissions, Python environment management, and debugging in production.

## Production Deployment

Later extended to a production multi-agent system at Aion Labs:



Deployed Obsidian vaults for 3 agents (Mirai, JJ, Chelsea) on Azure

Each agent maintains their own vault plus shared cross-agent context

RAG pipeline installed server-side with ChromaDB

All 3 agents read and write their own memory autonomously

Tested cross-session and cross-agent memory retrieval



## Results

TestResultCross-session memoryAgent remembered past mistakes without promptingCross-agent knowledgeJJ knew Chelsea's current work from shared vaultRAG semantic searchRelevant files returned for natural language queriesNightly auto-updateVault updated without human involvement

## Background

Built during my AI Engineering internship at Aion Research Corp in May 2026. No prior coding background — just curiosity and late nights debugging SSH connections and Python paths.

The memory architecture was validated by the Hyperagents research paper (arXiv:2603.19461) which found agents discover memory behaviors themselves when given the right scaffolding.

## Connect



GitHub: shreeja5060






