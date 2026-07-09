import express, { Request, Response } from "express";

// TODO: import your existing parsing logic here, e.g.:
// import { parseInvoice } from "./parser";

const app = express();
app.use(express.json({ limit: "10mb" }));

const PORT = process.env.PORT ? parseInt(process.env.PORT) : 8001;

app.get("/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", service: "invoice-parser" });
});

// The Manager App calls this endpoint to trigger a parse run.
// Wire your existing logic in here — this is the only integration point needed.
app.post("/run", async (req: Request, res: Response) => {
  try {
    // const result = await parseInvoice(req.body);
    const result = { message: "Wire your existing parser logic into this handler." };
    res.json({ status: "success", result });
  } catch (err) {
    res.status(500).json({ status: "error", message: (err as Error).message });
  }
});

app.listen(PORT, () => {
  console.log(`Invoice parser service listening on port ${PORT}`);
});
