<p align="center">
  <img src="docs/assets/logo.png" width="160" height="160" alt="The rust-anything crab">
</p>

<h1 align="center">rust-anything</h1>

<p align="center">by <a href="https://github.com/erkamyaman">erKam Yaman</a></p>

<p align="center">English · <a href="docs/README_TR.md">Türkçe</a> · <a href="docs/README_UK.md">Українська</a> · <a href="docs/README_ZH.md">简体中文</a> · <a href="docs/README_ZH-TW.md">繁體中文</a> · <a href="docs/README_DE.md">Deutsch</a> · <a href="docs/README_FR.md">Français</a> · <a href="docs/README_RU.md">Русский</a> · <a href="docs/README_JA.md">日本語</a> · <a href="docs/README_KO.md">한국어</a> · <a href="docs/README_AZ.md">Azərbaycanca</a> · <a href="docs/README_UZ.md">Oʻzbekcha</a> · <a href="docs/README_KK.md">Қазақша</a> · <a href="docs/README_KY.md">Кыргызча</a> · <a href="docs/README_TK.md">Türkmençe</a> · <a href="docs/README_TT.md">Татарча</a> · <a href="docs/README_UG.md">ئۇيغۇرچە</a> · <a href="docs/README_PT.md">Português</a> · <a href="docs/README_VI.md">Tiếng Việt</a></p>

<p align="center"><em>Rewrite your whole app in Rust. Keep it working the whole way.</em></p>

<p align="center"><em>CLIs, servers and libraries, piece by piece, checked against the original at every step.</em></p>

<p align="center">Node.js and TypeScript · Python · C · Go · Ruby · Java · PHP and C# in preview</p>

<p align="center">
  <a href="https://crates.io/crates/rust-anything"><img src="https://img.shields.io/crates/v/rust-anything?color=E2862A&label=crates.io" alt="crates.io version"></a>
  <a href="https://www.npmjs.com/package/rust-anything"><img src="https://img.shields.io/npm/v/rust-anything?color=E2862A&label=npm" alt="npm version"></a>
  <img src="https://img.shields.io/badge/languages-6%20%2B%202%20preview-E2862A" alt="6 languages, plus 2 in preview">
  <a href="#works-with"><img src="https://img.shields.io/badge/works%20with-5%20agents-E2862A" alt="Works with 5 agents"></a>
  <a href="https://github.com/erkamyaman/rust-anything/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/erkamyaman/rust-anything/ci.yml?branch=main&label=tests" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-E2862A" alt="MIT license"></a>
  <a href="https://github.com/erkamyaman/rust-anything"><img src="https://img.shields.io/github/stars/erkamyaman/rust-anything?style=social" alt="GitHub stars"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#languages">Languages</a> ·
  <a href="docs/how-it-works.md#how-it-works">How it works</a> ·
  <a href="docs/how-it-works.md#the-loop">The loop</a> ·
  <a href="docs/whole-apps.md#port-a-whole-app">Port a whole app</a> ·
  <a href="docs/how-it-works.md#hot-paths-keep-the-data-in-rust">Hot paths</a> ·
  <a href="docs/install.md#install">Install</a> ·
  <a href="docs/how-it-works.md#what-it-cant-catch">What it can't catch</a> ·
  <a href="docs/faq.md#faq">FAQ</a>
</p>

<p align="center">up to 20x faster · 38,251 recorded cases replayed · 0 mismatches · one command</p>

<p align="center">
  <img src="docs/assets/race.gif" alt="Typing user.profile into x18n's search over 50,000 keys: TypeScript spends 143 ms, the rust-anything batch 6.9 ms, with the same results at every keystroke." width="820">
  <br>
  <sub>Typing a query into x18n's search over 50,000 keys: the TypeScript original against the rust-anything batch, same results at every keystroke.</sub>
</p>

<table>
  <tr>
    <td width="25%" valign="top">
      <b>Record</b><br>
      <code>record</code> runs the original on generated edge cases, semantic traps and your own inputs, and saves what it returns or throws.
    </td>
    <td width="25%" valign="top">
      <b>Port</b><br>
      <code>bridge</code> generates the Rust crate and a wrapper, so callers keep the original API. You or your agent write the Rust.
    </td>
    <td width="25%" valign="top">
      <b>Check</b><br>
      <code>diff</code> replays every recorded case against the Rust, and nothing ships until they all match and <code>gate</code> passes.
    </td>
    <td width="25%" valign="top">
      <b>Lift</b><br>
      When replay passes with no fallback and every unit passes gate, <code>app lift</code> makes it a pure Rust app. The original is never touched.
    </td>
  </tr>
</table>

**Rewrite your whole app in Rust, one piece at a time.** rust-anything records what your
Node.js (TypeScript/JavaScript), Python, C, Go, Ruby or Java app does today, then checks every piece of the
Rust rewrite against that recording before it moves on, until the app is pure Rust. CLIs, HTTP
servers and libraries; your coding agent (or you) writes the Rust. It can only catch what the
recording covers: see [What it can't catch](docs/how-it-works.md#what-it-cant-catch). Only need the slow part fast?
Port just that, one hot path at a time:

| Real workload, same results as the original | Original | With rust-anything |
| --- | ---: | ---: |
| x18n's sidebar search, 50,000 keys (TypeScript, Node) | 10 ms per query | **0.5 ms: 20x faster** |
| The same search in the browser (wasm, one thread) | 10 ms | **0.95 ms: 11.5x** |
| `slugify` over 20,000 strings (Python) | 98 ms | **17x faster** |
| `Shellwords.shellescape` from Ruby's standard library, 50,000 values | 88 ms | **11.8x faster** |
| `Slugify` over 50,000 strings (Go) | 49 ms | **4x faster** |
| `slugify` over 50,000 strings (Java) | 43 ms | **3x faster** |

Measured on 4 cores; every number has a benchmark in [`demo/`](./demo) that first checks the
results are identical. Calling Rust once per small function is usually *slower* than a JIT;
rust-anything finds the loop worth moving, and moves it.

> rust-anything is an independent project, not affiliated with or endorsed by the Rust Project
> or the Rust Foundation. "Rust" is a trademark of the Rust Foundation.

> [!WARNING]
> `record` and `app record` run your original code, calling each function (or the whole app) on
> many generated inputs, and `app record` runs every case twice. `diff`, `gate` and `app replay`
> run the same cases again, on the port or the original. Code that writes files, talks to a
> database or calls the network does that once per case. Run them on a copy of the project, with a
> test database and no production credentials in the environment.

## Quick start

Paste this into Claude Code, Codex, Cursor, Gemini CLI or OpenCode and let your agent install it:

```text
Install rust-anything: run `cargo install rust-anything`, then `rust-anything setup`.
Tell me when to restart you.
```

Or yourself:

```sh
cargo install rust-anything   # from crates.io
rust-anything setup           # registers it with Claude Code, Codex, Cursor, Gemini CLI and OpenCode
```

No Rust toolchain yet? Prebuilt binaries for macOS, Linux and Windows are attached to each
[GitHub release](https://github.com/erkamyaman/rust-anything/releases), and for JavaScript
projects `npm install -g rust-anything` installs the same binary.

In Claude Code you can also install it as a plugin (the MCP server and the skill; the CLI above
must be on your `PATH`):

```text
/plugin install rust-anything --marketplace erkamyaman/rust-anything
```

`setup` adds the MCP server to each agent it finds and installs the workflow skill where the agent
reads skills. It keeps your other settings, is safe to run again, and `--remove` undoes it.
Then ask your agent, for example:

- *"Rewrite this CLI in Rust with rust-anything, end to end, and prove it behaves the same."*
- *"This search feels slow. Profile it with rust-anything and move the hot loop to Rust."*
- *"Plan a migration of `src/parser/` to Rust with rust-anything; port the first unit and prove it."*
- *"Bench the Rust port in `rust/text-rs` against the original and tell me whether to ship it."*

### Works with

| Agent | `rust-anything setup` adds |
| --- | --- |
| Claude Code | MCP server in `~/.claude.json`, skill in `~/.claude/skills/` |
| Codex | MCP server in `~/.codex/config.toml`, skill in `~/.codex/skills/` |
| Cursor | MCP server in `~/.cursor/mcp.json` |
| Gemini CLI | MCP server in `~/.gemini/settings.json` |
| OpenCode | MCP server in `~/.config/opencode/opencode.json` (`mcp.servers`), skill in `~/.config/opencode/skills/` |
| Any other MCP client | add `rust-anything mcp` as a stdio server by hand (see [Install](docs/install.md#install)) |

Before changing a file that exists, `setup` saves a copy beside it (`<file>.rust-anything.bak`).

To wire OpenCode up by hand, put the server in `~/.config/opencode/opencode.json` (`command` is
the whole argv) and copy [`skills/rust-anything/`](./skills/rust-anything) to
`~/.config/opencode/skills/rust-anything/`:

```json
{
  "mcp": {
    "servers": {
      "rust-anything": { "type": "local", "command": ["rust-anything", "mcp"] }
    }
  }
}
```

Or run the steps yourself:

<p align="center">
  <img src="docs/assets/terminal.gif" alt="rust-anything profile finds fuzzyScore in a loop, bridge --batch generates the Rust crate, gate passes with 2000/2000 recorded cases, and the benchmark shows 20.7x faster than TS." width="820">
  <br>
  <sub>The steps on x18n's <code>fuzzyScore</code>: <code>profile</code> finds the hot loop, <code>bridge --batch</code> generates the crate, <code>gate</code> passes, and the benchmark compares it with the TypeScript.</sub>
</p>

```sh
rust-anything profile . -- node bench.mjs              # what is hot, and who calls it
rust-anything bridge . src/fuzzy.ts --batch fuzzyScore:text
# write src/port.rs (or let your agent), then:
rust-anything record rust/fuzzy-rs && rust-anything build rust/fuzzy-rs
rust-anything diff rust/fuzzy-rs                       # every recorded case must match
rust-anything bench rust/fuzzy-rs                      # faster? the verdict says
rust-anything gate rust/fuzzy-rs                       # done means this passes
```

rust-anything does not translate code: your coding agent (Claude Code, Codex, Cursor, OpenCode, ...) or you write
the Rust. rust-anything supplies what an agent cannot guess reliably: where the time goes, what to port
first and in which order, a bridge so the rest of the code calls the Rust with its API unchanged,
the exact behavior the port must match, a safe way to ship it, and a gate that says when a port is
done.

## Languages

| Language | Unit | Bridge | Recorded and replayed by |
| --- | --- | --- | --- |
| TypeScript/JavaScript | folder or file | napi-rs or wasm-bindgen with a generated binary wire; classes and async included | Node, running the `.ts` sources |
| Python | package or module | PyO3 (abi3), direct conversion, typed exceptions | Python, importing the original |
| C | `.c` file | `extern "C"` functions with the original names and a header | the original compiled to a shared library, called through ctypes, one fork per case |
| Go | package | typed cgo calls and a generated binary wire, in a package with the original API | a generated Go driver, built as its own module |
| Ruby | file or folder of module functions | a magnus extension under the original modules | a generated Ruby driver |
| Java | package of `public static` methods | typed JNI and a generated binary wire, in wrapper classes with the original methods | a generated reflection driver |
| PHP (preview) | folder of functions and `public static` methods | coming next: PHP FFI over a C ABI | whole apps today: `app record`, `app replay` and the front door, for CLIs and servers (`php -S`) |
| C# (preview) | folder of `public static` methods | coming next: P/Invoke over a C ABI | whole apps today: `app record`, `app replay` and the front door, for CLIs and ASP.NET servers (`dotnet <app>.dll`) |

Every language except C also gets batch classes (`--batch`): the items cross once and stay in
Rust, and each call runs over all of them on all cores.

The language is detected from the repository (`go.mod`, `pom.xml`, a `.csproj` or `.sln`,
`pyproject.toml`, `Gemfile`, `composer.json`, `package.json`, else the most common source files);
`--lang` overrides it. Types come from the source: TS types, Python hints, C, Go, Java and C#
signatures, Ruby YARD tags, PHP types and phpdoc; untyped parameters used as numbers are inferred
as numbers.

PHP is in preview: `analyze` plans a PHP app (Composer packages and PSR-4 autoloading, risks
such as loose comparison and integer overflow into floats, Composer packages mapped to crates),
and a PHP CLI or server can be recorded, replayed and put behind a Rust front door. Porting its
units into Rust through PHP's FFI is the next step ([issue #2](https://github.com/erkamyaman/rust-anything/issues/2)).

C# is in preview the same way: `analyze` reads `.csproj` projects and their NuGet packages
(mapped to crates), resolves `using` directives to folders, and flags what C# does differently
(`decimal`, `dynamic`, LINQ's deferred queries, `Task`, `lock`, reflection). A C# CLI or ASP.NET
server can be recorded, replayed and put behind a Rust front door; porting units through P/Invoke
comes next.

## Learn more

- [How it works](docs/how-it-works.md): the loop, what `bridge` and `analyze` decide, hot paths, and what it can't catch
- [Port a whole app](docs/whole-apps.md): servers, CLIs and libraries, from the front door to `app lift`
- [Examples and case studies](docs/examples.md): x18n, and real code in six languages
- [Real-world ports](docs/real-world.md): json-server, Fuse.js, vercel/ms, with benchmarks
- [Install, update and develop](docs/install.md): every install method, Windows, and building from source
- [FAQ](docs/faq.md) · [Status](docs/STATUS.md) · [MCP tools](docs/tools.md)

## Sponsors

<p align="center">
  <a href="https://github.com/erkamyaman/rust-anything">rust-anything</a> is free and open source. If it helps your work, please consider sponsoring it.<br>
  Your support keeps development going.
</p>

<p align="center">
  <a href="https://coderabbit.ai">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/assets/sponsors/company-dark.svg">
      <img src="docs/assets/sponsors/company-light.svg" width="800" alt="Company sponsor: CodeRabbit">
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://github.com/sponsors/erkamyaman">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="docs/assets/sponsors/sponsors-dark.svg">
      <img src="docs/assets/sponsors/sponsors-light.svg" width="800" alt="Sponsors: Ali Yilmaz, Ashley Hunter, Fatih Uzuntaş">
    </picture>
  </a>
</p>

<p align="center">
  <a href="https://github.com/sponsors/erkamyaman"><img src="https://img.shields.io/badge/Become_a_sponsor-%E2%9D%A4-db61a2?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="Become a sponsor"></a>
</p>

## Contributing

Issues and pull requests are welcome; [CONTRIBUTING.md](./CONTRIBUTING.md) covers the setup, where
tests go, and how to add a language. Design choices and their reasons are in
[DECISIONS.md](./DECISIONS.md). Case studies of real ports are especially welcome. Please report
security problems privately ([SECURITY.md](./SECURITY.md)), and see the
[code of conduct](./CODE_OF_CONDUCT.md).

## License

[MIT](./LICENSE) © [Erkam Yaman](https://github.com/erkamyaman). Ports and generated code in your repository are yours.
