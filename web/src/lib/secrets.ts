import { SecretManagerServiceClient } from "@google-cloud/secret-manager";

const client = new SecretManagerServiceClient();

export async function accessSecret(secretName: string): Promise<string> {
  if (!process.env.GCP_PROJECT_ID) {
    throw new Error("GCP_PROJECT_ID is not set");
  }
  const name = `projects/${process.env.GCP_PROJECT_ID}/secrets/${secretName}/versions/latest`;
  const [version] = await client.accessSecretVersion({ name });
  const payload = version.payload?.data?.toString();
  if (!payload) {
    throw new Error(`Secret ${secretName} has no payload`);
  }
  return payload;
}
