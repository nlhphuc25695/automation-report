import { NextResponse } from "next/server";
import { z } from "zod";

import { prisma } from "@/lib/prisma";
import { requireAuth } from "@/lib/require-auth";

const clientSchema = z.object({
  clientId: z.string().min(1),
  name: z.string().min(1),
  objective: z.enum(["ecom", "lead", "branding", "social"]).default("ecom"),
  driveFolderId: z.string().optional(),
  sheetTemplateId: z.string().optional(),
  slidesTemplateId: z.string().optional(),
  metabaseEmbedUrl: z.string().optional(),
  accounts: z
    .array(
      z.object({
        platform: z.string().min(1),
        accountId: z.string().min(1),
      })
    )
    .default([]),
});

export async function GET() {
  const auth = await requireAuth();
  if (auth.response) return auth.response;

  const clients = await prisma.client.findMany({ include: { accounts: true } });
  return NextResponse.json(clients);
}

export async function POST(request: Request) {
  const auth = await requireAuth();
  if (auth.response) return auth.response;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
  const parsed = clientSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: "Validation failed", details: parsed.error.flatten() }, { status: 400 });
  }
  const data = parsed.data;

  try {
    const client = await prisma.client.create({
      data: {
        clientId: data.clientId,
        name: data.name,
        objective: data.objective,
        driveFolderId: data.driveFolderId,
        sheetTemplateId: data.sheetTemplateId,
        slidesTemplateId: data.slidesTemplateId,
        metabaseEmbedUrl: data.metabaseEmbedUrl,
        accounts: {
          create: data.accounts.map((acc) => ({
            platform: acc.platform,
            accountId: acc.accountId,
          })),
        },
      },
    });

    return NextResponse.json(client, { status: 201 });
  } catch {
    return NextResponse.json({ error: "Failed to create client" }, { status: 500 });
  }
}
