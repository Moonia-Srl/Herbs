# Herbs

### A set of CLI tool to automate processes related to Solana's NFTs

## Description

This repository provides some utility scripts written in Python to automate and complex process related to NFTs minted on the Solana blockchain.

One of such example is the minting process of an entire collection using Metaplex' Candy Machine implementation. This task requires to deploy the Candy Machine, uploads the assets and metadata to a decentralized storage provider (Arweawe, IPFS, Pinata, ...) and then mint one or more tokens.

This multistage process is automated bu the script `peppermint.py` that wraps the Candy Machine CLI and provides a higher-level API.

## Scripts overview

- `peppermint.py`: Used to automate the minting process for any given collection of NFTs.
- `eucaliptus.py`: Used to transfer in bulk the owned NFTs of a given collection using a .csv file as template
- `lavender.py`: Used only in development purges all the NFTs (Data account & SPL Token) from the current wallet in the Solana CLI tool.
