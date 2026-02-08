import { Router } from "express";
import {
    Keypair,
    Networks,
    TransactionBuilder,
    Operation,
    Asset,
    BASE_FEE,
    rpc,
} from "@stellar/stellar-sdk";

const router = Router();

const RPC_URL = process.env.RPC_URL || "https://soroban-testnet.stellar.org";
const NETWORK_PASSPHRASE = process.env.NETWORK_PASSPHRASE || Networks.TESTNET;

// POST /deployer/single-release - Generate unsigned XDR for contract deployment
router.post("/single-release", async (req, res) => {
    try {
        const {
            signer,
            engagementId,
            title,
            description,
            roles,
            amount,
            platformFee,
            milestones,
            trustline
        } = req.body;

        // Validate required fields
        if (!signer || !engagementId || !title || !description || !roles || 
            amount === undefined || platformFee === undefined || !milestones || !trustline) {
            return res.status(400).json({
                error: "Missing required fields",
                required: [
                    "signer", "engagementId", "title", "description", 
                    "roles", "amount", "platformFee", "milestones", "trustline"
                ]
            });
        }

        // Validate roles
        const requiredRoles = ["approver", "serviceProvider", "platformAddress", 
                              "releaseSigner", "disputeResolver", "receiver"];
        for (const role of requiredRoles) {
            if (!roles[role]) {
                return res.status(400).json({
                    error: `Missing required role: ${role}`
                });
            }
        }

        // Validate milestones
        if (!Array.isArray(milestones) || milestones.length === 0) {
            return res.status(400).json({
                error: "Milestones must be a non-empty array"
            });
        }

        // Validate trustline
        if (!trustline.symbol || !trustline.address) {
            return res.status(400).json({
                error: "Trustline must include symbol and address"
            });
        }

        // Create RPC server
        const server = new rpc.Server(RPC_URL, { allowHttp: false });

        // Get source account
        const sourceKeypair = Keypair.fromPublicKey(signer);
        const sourceAccount = await server.getAccount(signer);

        // Create the asset for USDC
        const asset = new Asset(trustline.symbol, trustline.address);

        // Build transaction with payment operation as a placeholder
        // In a real implementation, this would deploy a smart contract
        const transaction = new TransactionBuilder(sourceAccount, {
            fee: BASE_FEE,
            networkPassphrase: NETWORK_PASSPHRASE,
        })
            // Add memo with engagement details
            .addMemo({
                type: "text",
                value: `${engagementId}:${title.substring(0, 20)}`
            })
            // Placeholder operation - in real implementation would be contract deployment
            .addOperation(
                Operation.payment({
                    destination: roles.receiver,
                    asset: asset,
                    amount: amount.toString(),
                })
            )
            .setTimeout(300)
            .build();

        // Get the unsigned XDR
        const xdr = transaction.toXDR();

        res.json({
            success: true,
            xdr: xdr,
            message: "Unsigned XDR generated successfully. Please sign it using Stellar Laboratory.",
            details: {
                engagementId,
                title,
                amount,
                platformFee,
                milestonesCount: milestones.length,
                network: "testnet",
                requiresSignature: signer
            }
        });
    } catch (error) {
        console.error("Error generating XDR:", error);
        res.status(500).json({ 
            error: error.message,
            details: "Failed to generate unsigned XDR transaction"
        });
    }
});

// POST /deployer/submit - Submit signed XDR to the network
router.post("/submit", async (req, res) => {
    try {
        const { signedXdr } = req.body;

        if (!signedXdr) {
            return res.status(400).json({
                error: "Missing required field: signedXdr"
            });
        }

        // Create RPC server
        const server = new rpc.Server(RPC_URL, { allowHttp: false });

        // Submit the signed transaction
        const transactionResult = await server.sendTransaction({
            xdr: signedXdr
        });

        // Poll for transaction result
        let status = transactionResult.status;
        let hash = transactionResult.hash;

        if (status === "PENDING") {
            // Wait for confirmation
            let attempts = 0;
            const maxAttempts = 10;

            while (attempts < maxAttempts) {
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                try {
                    const txStatus = await server.getTransaction(hash);
                    if (txStatus.status === "SUCCESS") {
                        status = "SUCCESS";
                        break;
                    } else if (txStatus.status === "FAILED") {
                        status = "FAILED";
                        break;
                    }
                } catch (e) {
                    // Transaction might not be available yet
                }
                
                attempts++;
            }
        }

        res.json({
            success: status === "SUCCESS",
            transactionHash: hash,
            status: status,
            message: status === "SUCCESS" 
                ? "Transaction submitted successfully! Verify on Stellar Expert." 
                : "Transaction submitted but status is " + status,
            stellarExpertUrl: `https://stellar.expert/explorer/testnet/tx/${hash}`
        });
    } catch (error) {
        console.error("Error submitting XDR:", error);
        res.status(500).json({ 
            error: error.message,
            details: "Failed to submit signed XDR transaction"
        });
    }
});

export default router;
