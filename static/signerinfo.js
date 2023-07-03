import { ethers } from "https://cdn-cors.ethers.io/lib/ethers-5.7.2.esm.min.js";

const CONTRACT_ADDRESS = '0x711BD4B4f32ca39cbfDd05CA19D063632f4F50B4';
const CONTRACT_ABI = [
     {
      "inputs": [
        {
          "internalType": "string",
          "name": "initialSentence",
          "type": "string"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "getSentence",
      "outputs": [
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "newSentence",
          "type": "string"
        }
      ],
      "name": "setSentence",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
    ];

const provider = new ethers.providers.Web3Provider(window.ethereum);
await provider.send("eth_requestAccounts", []);

const signer = provider.getSigner()
const contract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);
async function sendTransaction(message) {

  // create transaction
  const unsignedTrx = await contract.populateTransaction.setSentence(message);
  console.log('Transaction created');

  // send transaction via signer so it's automatically signed
  const txResponse = await signer.sendTransaction(unsignedTrx);

  console.log(`Transaction signed and sent: ${txResponse.hash}`);
  
  // wait for transaction to be processed
  await txResponse.wait(1);
}
// expose the transaction to the clientside callback
window.sendTransaction = sendTransaction

