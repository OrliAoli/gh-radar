<p align="center">
  <img src="https://raw.githubusercontent.com/EL4CTEO/fast-anything/main/docs/assets/wordmark.png" alt="fast-anything" width="520">
</p>

<p align="center"><b>Don't rewrite it in Rust. Rewrite the 5% that's slow.</b></p>

<p align="center">
  <a href="https://trendshift.io/repositories/371252" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/371252/daily?language=Rust" alt="EL4CTEO/fast-anything: Rust repository of the day on Trendshift" width="250" height="55"></a>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@el4cteo/fast-anything"><img src="https://img.shields.io/npm/v/@el4cteo/fast-anything?color=f74c00&label=npm" alt="npm"></a>
  <a href="https://crates.io/crates/fast-anything"><img src="https://img.shields.io/crates/v/fast-anything?color=f74c00" alt="crates.io"></a>
  <a href="https://github.com/EL4CTEO/fast-anything/actions/workflows/ci.yml"><img src="https://github.com/EL4CTEO/fast-anything/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/Python%20%C2%B7%20Node%20%C2%B7%20TypeScript%20%C2%B7%20Ruby%20%C2%B7%20Java%20%C2%B7%20Kotlin%20%C2%B7%20Go%20%C2%B7%20PHP%20%C2%B7%20C%20%C2%B7%20C%2B%2B%20%C2%B7%20C%23%20%C2%B7%20R-2563eb" alt="Python, Node, TypeScript, Ruby, Java, Kotlin, Go, PHP, C, C++, C#, R">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin-d97757" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/MCP-server-555" alt="MCP server">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-555" alt="MIT"></a>
</p>

Most of an app's runtime sits in a few functions. **fast-anything** finds them, has your coding agent port *only those* to Rust, proves the port returns the same results on real recorded calls, and swaps it in. Reversible, one function at a time.

<p align="center"><img src="https://raw.githubusercontent.com/EL4CTEO/fast-anything/main/docs/assets/demo.gif" alt="fast-anything go --agent claude -- python app.py" width="820"></p>

## Install

```sh
npm i -g @el4cteo/fast-anything      # or: cargo install fast-anything
```

The command is `fast-anything`. Scanning needs only your app's runtime; porting needs Rust ([rustup](https://rustup.rs)). `fast-anything doctor` checks both.

## Use

```sh
fast-anything go --agent claude -- python app.py
```

Use the command you normally run your app with (`node app.ts`, `go run .`, `gradle run`, `dotnet run`, …). `--agent` takes `claude`, `codex` or any command that reads a prompt on stdin.

Step by step:

| command | what it does |
|---|---|
| `scan -- <cmd>` | profiles the app and ranks functions by time and portability |
| `port [id]` | records real calls and creates a one-function Rust crate with a `TASK.md` |
| `verify` | builds the port and replays every recorded call against it |
| `enable` / `disable` | switches the Rust in or out |
| `bench` | times the whole app, original vs Rust, with an A/A noise control |
| `report` | markdown + SVG card for your PR |
| `status` / `doctor` | where things stand / what's installed |

Useful `scan` flags: `--duration 30` for servers and GUIs, `--calibrate` to measure the profiler's overhead, `--explain` to check the setup without running. Every command takes `--json`.

## Proof, not vibes

<p align="center"><img src="https://raw.githubusercontent.com/EL4CTEO/fast-anything/main/docs/assets/verify.gif" alt="verify catches a wrong port" width="820"></p>

- Every port is replayed against up to 500 real calls, plus edge cases (NaN, ±infinity, -0.0, empty, non-ASCII, bigger inputs) answered by the original.
- Every 5th call is held out from the agent, so a port can't special-case what it was shown.
- Nothing is enabled until all cases match, and a port that's slower per call stays off.
- `FAST_ANYTHING_DISABLE=1` runs the original any time.

## Results

Real runs on an i5-10500, Windows 11 (C and C++: a GitHub Actions Linux runner). Reproduce them from [`examples/`](examples).

| app | before | after |
|---|---|---|
| Python fuzzy dedupe | 4.91s | **42ms, 116×** |
| PHP fuzzy dedupe | 2.94s | **53ms, 55×** |
| Go fuzzy dedupe | 3.02s | **144ms, 21×** |
| TypeScript fuzzy dedupe | 3.11s | **155ms, 20×** |
| Ruby fuzzy dedupe | 3.13s | **228ms, 14×** |
| C# fuzzy dedupe | 4.03s | **312ms, 13×** |
| C mandelbrot | 431ms | **127ms, 3.4×** |
| Java fuzzy dedupe | 3.50s | **1.18s, 3×** (11× on the function; the rest is JVM startup) |
| C++ fuzzy dedupe | 3.02s | **1.09s, 2.7×** |

It ports the outermost loop it can, so the app crosses into Rust once instead of millions of times.

## Languages

| language | how it's run |
|---|---|
| Python 3.10+ | `python app.py` (PyO3) |
| JavaScript / TypeScript | `node` 22+, `bun`, `deno run -A` (napi-rs) |
| Ruby 3.3+ | `ruby app.rb` |
| Java 22+ | `java App.java`, Maven, Gradle |
| Kotlin/JVM | Gradle, `src/main/kotlin`, JDK 22+ |
| Go 1.22+ | `go run .` |
| PHP 8.1+ | `php app.php` (FFI extension) |
| C / C++ | gcc, clang, icx/icpx |
| C# / .NET 8+ | `dotnet run -c Release` |
| R 4.0+ | `Rscript app.R` |

Python and JS/TS use native bindings; the rest call the port through one C entry point, with no headers or extra tools. It ports top-level, deterministic functions that take plain data (numbers, strings, lists, maps, arrays). `scan` says why anything else can't move yet.

## Android

Android apps run on ART, so they're profiled on the device instead:

```sh
fast-anything scan --android com.example.app --duration 10
```

It ranks the app's own methods with simpleperf over adb (debuggable or profileable build). Device measurements (`import gfxinfo`, `perfetto`, `simpleperf`, `json`) go in the report in their own section. Ranking only: Android code isn't ported, and ART times are never compared with host ones.

## Agents

- **Claude Code**: `/plugin marketplace add EL4CTEO/fast-anything`, then `/plugin install fast-anything@fast-anything`
- **Codex**: `codex plugin marketplace add EL4CTEO/fast-anything`
- **MCP server** (any client): `claude mcp add fast-anything -- fast-anything mcp`
- **Skill**: [`skills/fast-anything`](skills/fast-anything/SKILL.md) teaches any agent the loop

## Sponsors

fast-anything is free and open source. If it saves you time, sponsoring keeps it maintained.

<p>
  <a href="https://github.com/sponsors/EL4CTEO"><img src="https://img.shields.io/badge/Become_a_sponsor-%E2%9D%A4-db61a2?logo=githubsponsors&logoColor=white" alt="Become a sponsor"></a>
</p>

## License

MIT
