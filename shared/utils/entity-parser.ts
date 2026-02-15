export const parseEntityInput = (raw: string): string[] => {
  return raw
    .split(/[\n,;]+/)
    .map((token) => token.trim())
    .filter(Boolean);
};
