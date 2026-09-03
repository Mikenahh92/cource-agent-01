"""Generate a deterministic access log for the analyzer (fixed seed)."""
import random
import sys

PATH = "data/access.log"
LEVELS = ["INFO", "WARN", "ERROR", "DEBUG"]
ENDPOINTS = ["/api/users", "/api/orders", "/api/items", "/health", "/metrics", "/login"]
STATUS = [200, 201, 204, 400, 401, 404, 500]


def main(n=12000, path=PATH):
    random.seed(42)
    lines = []
    t = 1_700_000_000
    for i in range(n):
        t += random.randint(1, 30)
        line = (f"{t} {random.choice(LEVELS)} {random.choice(ENDPOINTS)} "
                f"{random.choice(STATUS)} {random.randint(1, 500)}ms")
        lines.append(line)
    # ~10% exact duplicates — the analyzer is supposed to dedupe these
    lines += random.sample(lines, n // 10)
    random.shuffle(lines)
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} lines to {path}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 12000)
