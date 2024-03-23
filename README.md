<div>
    <img src="https://avatars.githubusercontent.com/u/52098353" align="left" width="110" style="margin-right: 15px"/>
    <h1>   
        🌐 Unigrid Networks
    </h1>
    <p> This repository contains information on Unigrid public networks </p>
    <br>
</div>

| Chain ID                              | Type      | Status     | Version       | Notes                     |
|---------------------------------------|-----------|------------|---------------|---------------------------|
| [unigrid-testnet-5](./unigrid-testnet-5) | `testnet` | **Active** | `v0.0.15` | Testnet                   |
| [unigrid-testnet-4](./unigrid-testnet-4) | `testnet` | **Deprecated** | `v0.0.10` | Testnet                   |
| [unigrid-testnet-3](./unigrid-testnet-3) | `testnet` | **Deprecated** | `v0.0.9` | Testnet                   |
| [unigrid-testnet-2](./unigrid-testnet-2) | `testnet` | **Deprecated** | `v0.0.8` | Testnet                   |
| [unigrid-testnet-1](./unigrid-testnet-1) | `testnet` | **Deprecated** | `v0.0.1` | Testnet                   |


## Testnets

### Overview

**Testnets** are specialized blockchain environments designed specifically for testing and development purposes. Unlike the live blockchain, known as the mainnet, testnets offer a safe and isolated space where developers can experiment with new code, features, and functionalities without the risk of impacting the actual blockchain or its real-world assets.

### Characteristics of Testnets

1. **Sandbox Environment**: Testnets serve as a sandbox, providing a realistic blockchain experience for testing. Here, developers can freely test their applications, smart contracts, and various blockchain interactions without the fear of costly mistakes or loss of real assets.

2. **Persistent Nature**: Most testnets are persistent, meaning they are maintained over extended periods. This longevity allows for continuous development cycles, long-term experiments, and stability in testing environments.

3. **Integrated Services**: To enhance the testing experience, testnets often include a range of integrated services:
    - **Relayers**: These are services that facilitate communication and asset transfer between different testnets or between a testnet and the mainnet.
    - **Frontends**: User interfaces are provided to interact with the testnet, allowing for easy testing of blockchain functionalities from a user's perspective.
    - **Explorers**: Blockchain explorers specific to testnets help in tracking transactions, blocks, and other on-chain activities, enabling detailed analysis and debugging.
    - **Snapshot Services**: These services capture the state of the testnet at specific intervals, useful for resetting tests or analyzing historical data.

### Purpose and Benefits

- **Risk-Free Testing**: Testnets offer a risk-free zone to conduct trials and errors, crucial for the development and fine-tuning of blockchain projects.
- **Network Testing**: They provide an environment to test the network's response to changes, like upgrades or forks, before implementation on the mainnet.
- **Learning and Education**: Testnets are excellent tools for education and training, allowing new developers to learn blockchain technologies without financial risks.

### Conclusion

Testnets are an indispensable part of the blockchain development ecosystem. By simulating the conditions of the mainnet while eliminating risks, they play a critical role in ensuring the robustness, security, and efficiency of blockchain solutions.

### 🟧 unigrid-testnet-4

| Chain ID         | `unigrid-testnet-5`                                      |
|------------------|----------------------------------------------------|
| Paxd version | `v0.0.15`                                      |
| Genesis          | [genesis.json](https://raw.githubusercontent.com/unigrid-project/unigrid-cosmos-networks/master/unigrid-testnet-5/genesis/genesis.json) |
| RPC              | <https://rpc-two-testnet.unigrid.org/>                 |
| gRPC             | <grpc-testnet.unigrid.org:9090>                |
| REST             | <https://rest-two-testnet.unigrid.org/>                 |
| Faucet           | [UGD faucet](https://docs.unigrid.org/docs/testnet/jointestnet/)            |
| Explorer         | <https://explorer-devnet.unigrid.org/>            |
<!-- | Snapshots        | <https://unigrid.org>           | -->


### 🌱 Seed

| Node          | ID                                                                                                                                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Unigrid Seed | `96de577a45c68d8d539236334eb097515b63c70a@207.180.254.48:26656` <br/> `e339ab8163a2774fccbc78ff09ffbf0991adc310@38.242.156.2:26656` <br/> `06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656`   <br/> `fe420bfcff68beff824d9777bfe6ce1aa4cf8f43@149.102.133.13:26656`                                                            |


Add the Node ID in your `p2p.seeds` section of you `config.toml`:


> in our automated script these are passed in during paxd startup: [Install Guide](https://github.com/unigrid-project/unigrid-cosmos-networks/tree/master/unigrid-testnet-4)

```toml
#######################################################
###           P2P Configuration Options             ###
#######################################################
[p2p]

# ...

# Comma separated list of seed nodes to connect to
seeds = "8cc2192d6de0936632e0818c3b030a465a40d2dc@149.102.133.13:26656,06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656,06ed85d8b34ca3a4275072894fc297dce416b708@194.233.95.48:26656"
```

🚰 Faucet
The unigrid-testnet faucet is available via our [discord server](https://docs.unigrid.org/docs/testnet/jointestnet/)

If you are an validator needing more funds, you can request them via this [form](https://forms.gle/Ubv2u6T1AWgWkTRS9).
