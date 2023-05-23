export function SynthUrl(
  base: string[],
  kwargs?: Record<string, string | string[] | number | number[]>
): string {
  if (kwargs === undefined) {
    return "/api/" + base.join("/");
  }
  let params = [];
  for (const [key, value] of Object.entries(kwargs)) {
    params.push(`${key}=${value}`);
  }
  return "/api/" + base.join("/") + `?${params.join("&")}`;
}
