# Lab 5 – Issues found in `billing_system.py`

Tools: Pylint 4.x, Bandit 1.9, Flake8 7.x. Before: Pylint **4.43/10**. After: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**.
Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Card encrypted with AES-ECB and a hardcoded key | Security (High) | 15, 72–74 | ECB gives identical ciphertext for identical cards (demo printed `True`), and the key is in source code. Bandit B413 also flags the deprecated `Crypto` import. | Use AES-GCM from `cryptography` with a random 12-byte nonce per call; read the key from the `CARD_KEY` environment variable. |
| Hardcoded webhook secret | Security (High) | 14 | Bandit B105: `whsec_live_...` is committed to the repo. | Load from the `WEBHOOK_SECRET` environment variable (random fallback for the demo). |
| XSS in invoice template | Security (High) | 84–86 | Mako renders `${user}` unescaped, so `<b onmouseover=alert(1)>` appeared as live HTML (Bandit B702). | `Template(..., default_filters=["h"])` HTML-escapes all values. |
| Unsafe XML parsing (XXE / entity expansion) | Security (Medium) | 80–82 | `lxml.etree.fromstring` on untrusted webhook data resolves entities. | Use `defusedxml.ElementTree.fromstring`. |
| Weak randomness for coupon codes | Security (Medium) | 3, 67 | Bandit B311: `random` is predictable, so coupon codes can be guessed. | Use `secrets.choice`. |
| Non-constant-time signature compare | Security (Medium) | 78 | `==` on HMAC digests leaks timing information. | `hmac.compare_digest`. |
| `assert` used for validation | Security / Bug (Low) | 85 | Bandit B101: asserts are stripped with `python -O`, so negative amounts would pass. | Raise `ValueError`. |
| Retry loop runs 4 times | Bug (logic) | 52 | `attempts <= MAX_ATTEMPTS` with a max of 3 gave 4 attempts. | `attempts < MAX_ATTEMPTS`, and `break` on success. |
| Refund function broken | Bug (logic) | 58–64 | `return` inside `finally` (Pylint W0134/W0150/E0601), always refunds the full price (999), and the `print` is unreachable. | Remove the try/finally; refund the unused part: `price * (30 - days_used) / 30`; validate `days_used`. |
| Coupon over 100% gives negative invoice | Bug (logic) | 33 | `FRIENDS150` produced `-294.41`. | Clamp percent to 0–100. |
| Coupon rejected on its expiry day | Bug (logic) | 31 | `today >= expires` rejects the last valid day. | `today > expires`. |
| `invoiceAmount` crashes without a date | Bug (logic) | 35–38 | `today=None` is passed to the comparison, raising `TypeError`. | Default to `date.today()`. |
| Trial end off by one | Bug (logic) | 25 | A 14-day trial from 09-01 was not "over" on 09-15. | `>=` instead of `>`. |
| Next billing date breaks | Bug (logic) | 41 | `month + 1` fails in December and on 31 January. | Use `calendar.monthrange` and clamp the day. |
| Proration assumes a 30-day month | Bug (logic) | 48 | February has 28 days; also unrounded money values (`166.666…`). | Divide by the real days in the period and `round(..., 2)`. |
| Unrounded money values | Bug (logic) | 33, 38, 48 | Output like `529.938` and `588.8199999999999`. | `round(x, 2)`. |
| Unused imports `os`, `sys`; multiple imports on one line | Style | 1 | Pylint W0611/C0410, Flake8 F401/E401. | Remove unused imports; one import per line (`os` is now actually used for env vars). |
| `== None` comparison | Style | 29 | Pylint C0121, Flake8 E711. | `is None`. |
| `dict()` / `list()` / `set([...])` calls | Style | 16, 21, 70 | Pylint R1735, R1734, R1718. | Use `{}`, `[]` and a set comprehension. |
| camelCase function names | Style | 24–84 | Pylint C0103 (13 functions). | Renamed to snake_case. |
| Missing docstrings | Style | all | Pylint C0114/C0116. | Added module and function docstrings. |
| Line length and blank lines | Style | many | Flake8 E501, E302, E305; Pylint C0301. | Wrapped lines to 79 chars, 2 blank lines between functions. |
| Code runs on import | Quality | 107 | `main()` ran at import time. | `if __name__ == "__main__":`. |
