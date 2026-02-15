export const parseEntityInput = (raw: string): string[] =>
  raw
    .split(/[\n,;]+/)
    .map((token) => token.trim())
    .filter(Boolean);
