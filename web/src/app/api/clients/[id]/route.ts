import { NextResponse } from "next/server";
import { z } from "zod";

import { prisma } from "@/lib/prisma";
import { requireAuth } from "@/lib/require-auth";

const updateSchema = z.object({
  name: z.string().optional(),
  objective: z.enum(["ecom", "lead", "branding", "social"]).optional(),
  driveFolderId: z.string().optional(),
  sheetTemplateId: z.string().optional(),
  slidesTemplateId: z.string().optional(),
  metabaseEmbedUrl: z.string().optional(),
});

export async function GET(_: Request, { params }: { params: { id: string } }) {
  const auth = await requireAuth();
  if (auth.response) return auth.response;

  const client = await prisma.client.findUnique({
    where: { id: params.id },
    include: { accounts: true, runs: true },
  });

  if (!client) return NextResponse.json({ error: "Not found" }, { status: 404 });
  return NextResponse.json(client);
}

export async function PATCH(request: Request, { params }: { params: { id: string } }) {
  const auth = await requireAuth();
  if (auth.response) return auth.response;

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
  const parsed = updateSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: "Validation failed", details: parsed.error.flatten() }, { status: 400 });
  }

  try {
    const client = await prisma.client.update({ where: { id: params.id }, data: parsed.data });
    return NextResponse.json(client);
  } catch {
    return NextResponse.json({ error: "Failed to update client" }, { status: 500 });
  }
}

export async function DELETE(_: Request, { params }: { params: { id: string } }) {
  const auth = await requireAuth();
  if (auth.response) return auth.response;

  await prisma.$transaction([
    prisma.adAccount.deleteMany({ where: { clientId: params.id } }),
    prisma.runLog.deleteMany({ where: { clientId: params.id } }),
    prisma.client.delete({ where: { id: params.id } }),
  ]);
  return NextResponse.json({ ok: true });
}
