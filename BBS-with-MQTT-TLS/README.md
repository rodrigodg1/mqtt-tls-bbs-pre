[![MATTR](./docs/assets/mattr-logo-square.svg)](https://github.com/mattrglobal)

# BBS-signatures with MQTT without TLS

This repository is the home to a performant multi-message digital signature algorithm implementation which supports
deriving zero knowledge proofs that enable selective disclosure from the originally signed message set.

[BBS+ Signatures](https://github.com/mattrglobal/bbs-signatures-spec) are a digital signature algorithm originally born from the work on
[Short group signatures](https://crypto.stanford.edu/~xb/crypto04a/groupsigs.pdf) by Boneh, Boyen, and Shachum which was
later improved on in [Constant-Size Dynamic k-TAA](http://web.cs.iastate.edu/~wzhang/teach-552/ReadingList/552-14.pdf)
as BBS+ and touched on again in section 4.3 in
[Anonymous Attestation Using the Strong Diffie Hellman Assumption Revisited ](https://www.researchgate.net/publication/306347781_Anonymous_Attestation_Using_the_Strong_Diffie_Hellman_Assumption_Revisited).

BBS+ signatures require a
[pairing-friendly curve](https://tools.ietf.org/html/draft-irtf-cfrg-pairing-friendly-curves-03), this library includes
support for [BLS12-381](https://tools.ietf.org/html/draft-irtf-cfrg-pairing-friendly-curves-03#section-2.4).

BBS+ Signatures allow for multi-message signing whilst producing a single output signature. With a BBS signature, a
[proof of knowledge](https://en.wikipedia.org/wiki/Proof_of_knowledge) based proof can be produced where only some of
the originally signed messages are revealed at the discretion of the prover.

For more details on the signature algorithm please refer to [here](https://github.com/mattrglobal/bbs-signatures-spec).

## Getting started

To use this package within your project simply run

```
npm install @mattrglobal/bbs-signatures
```

Or with [Yarn](https://yarnpkg.com/)

```
yarn add @mattrglobal/bbs-signatures
```

### Prerequisites

The following is a list of dependencies:

- [Yarn](https://yarnpkg.com/)
- [Rust](https://www.rust-lang.org/)
- [Mosquitto](https://mosquitto.org/download/)
- [MQTT](https://www.npmjs.com/package/mqtt)

## Example

- [Example 1](https://github.com/rodrigodg1/js-mqtt-tls-bbs/tree/main/BBS-with-MQTT-and-TLS/sample/ts-node)

or

```
cd sample/ts-node
```
