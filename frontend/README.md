# BB84 Quantum Key Distribution Protocol (Python Implementation)
## Overview

This project implements the BB84 Quantum Key Distribution (QKD) protocol, one of the first and most well-known quantum cryptography protocols. The protocol allows two parties (traditionally called Alice and Bob) to securely generate a shared cryptographic key while detecting potential eavesdropping.

This implementation simulates the BB84 protocol using Python and provides a simple interface for running the protocol and observing the key exchange process.

## How It Works

### The BB84 protocol works through several steps:

* _Bit Generation_ – Alice generates a random sequence of bits.

* _Basis Selection_ – Alice encodes each bit using a randomly chosen basis (rectilinear or diagonal).

* _Transmission_ – The encoded bits are sent to Bob.

* _Measurement_ – Bob measures each qubit using randomly chosen bases.

* _Basis Comparison_ – Alice and Bob publicly compare bases and discard mismatched measurements.

* _Key Extraction_ – The remaining bits form the shared secret key.

* _Eavesdropping Detection_ – A subset of the key can be compared to detect interception.

## Technologies Used

###### Python – core protocol implementation

###### Node.js / npm – frontend interface

## How to Run the Project

###### Open the terminal in the project directory and run:

### `python app.py`

###### Open a second terminal in the 'frontend' directory and run:

### `npm start`


This implementation is intended for educational purposes, demonstrating how the BB84 protocol works conceptually.
## Authors

Beatrice CODINĂ
