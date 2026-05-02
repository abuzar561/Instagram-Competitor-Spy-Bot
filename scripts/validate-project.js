const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const failures = [];

const requiredFiles = [
  "README.md",
  "LICENSE",
  "CHANGELOG.md",
  "CONTRIBUTING.md",
  "SECURITY.md",
  ".editorconfig",
  ".env.example",
  ".gitattributes",
  ".gitignore",
  ".github/workflows/validate.yml",
  "requirements.txt",
  "spy.py",
  "src/__init__.py",
  "src/instagram_spy_bot.py",
  "workflow/instagram-spy-google-sheets.json",
  "workflow/README.md",
  "docs/PAYLOAD.md",
  "docs/SETUP.md",
  "docs/TROUBLESHOOTING.md",
  "docs/WORKFLOW.md",
  "examples/payload.example.json"
];

const requiredPayloadFields = [
  "competitor",
  "post_shortcode",
  "post_url",
  "image_url",
  "caption",
  "likes",
  "comments",
  "followers",
  "engagement_rate",
  "is_viral",
  "viral_threshold_percent",
  "taken_at",
  "scraped_at"
];

function fail(message) {
  failures.push(message);
}

function readText(relativePath) {
  return fs.readFileSync(path.join(root, relativePath), "utf8");
}

function listFiles(directory) {
  const entries = fs.readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const fullPath = path.join(directory, entry.name);

    if ([".git", ".venv", "node_modules", "__pycache__"].includes(entry.name)) {
      return [];
    }

    if (entry.isDirectory()) {
      return listFiles(fullPath);
    }

    return [fullPath];
  });
}

function isTextFile(filePath) {
  const textBasenames = new Set([
    ".editorconfig",
    ".env.example",
    ".gitattributes",
    ".gitignore",
    "LICENSE"
  ]);

  return [
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yml"
  ].includes(path.extname(filePath)) || textBasenames.has(path.basename(filePath));
}

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(root, file))) {
    fail(`Missing required file: ${file}`);
  }
}

const workflowPath = path.join(root, "workflow/instagram-spy-google-sheets.json");
let workflow;

try {
  workflow = JSON.parse(fs.readFileSync(workflowPath, "utf8"));
} catch (error) {
  fail(`Workflow JSON is invalid: ${error.message}`);
}

if (workflow) {
  const nodeNames = new Set((workflow.nodes || []).map((node) => node.name));
  const requiredNodes = [
    "Instagram Post Webhook",
    "Log Post Snapshot",
    "Build Viral Alert",
    "Send Discord Alert"
  ];

  for (const nodeName of requiredNodes) {
    if (!nodeNames.has(nodeName)) {
      fail(`Workflow missing node: ${nodeName}`);
    }
  }

  if (workflow.active !== false) {
    fail("Workflow export should be inactive for safe public import.");
  }

  if (workflow.id || workflow.versionId || workflow.tags) {
    fail("Workflow should not include root export identifiers.");
  }

  if (workflow.meta && workflow.meta.instanceId) {
    fail("Workflow should not include n8n instance metadata.");
  }

  const workflowText = JSON.stringify(workflow);

  if (/"credentials"\s*:/.test(workflowText)) {
    fail("Workflow should not include exported credential bindings.");
  }

  if (/"webhookId"\s*:/.test(workflowText)) {
    fail("Workflow should not include exported webhook IDs.");
  }

  for (const [sourceNode, outputs] of Object.entries(workflow.connections || {})) {
    if (!nodeNames.has(sourceNode)) {
      fail(`Workflow connection references missing source node: ${sourceNode}`);
    }

    for (const outputGroup of outputs.main || []) {
      for (const output of outputGroup) {
        if (!nodeNames.has(output.node)) {
          fail(`Workflow connection references missing target node: ${output.node}`);
        }
      }
    }
  }
}

try {
  const payload = JSON.parse(readText("examples/payload.example.json"));
  for (const field of requiredPayloadFields) {
    if (!Object.prototype.hasOwnProperty.call(payload, field)) {
      fail(`Example payload missing field: ${field}`);
    }
  }
} catch (error) {
  fail(`Example payload JSON is invalid: ${error.message}`);
}

const source = fs.existsSync(path.join(root, "src/instagram_spy_bot.py"))
  ? readText("src/instagram_spy_bot.py")
  : "";

for (const token of ["COMPETITORS", "N8N_WEBHOOK_URL", "POSTS_TO_CHECK", "VIRAL_THRESHOLD_PERCENT"]) {
  if (!source.includes(token)) {
    fail(`Python monitor should support ${token}.`);
  }
}

const legacyTargetRegex = new RegExp(["mab" + "uzar", "abuzar" + "5533"].join("|"), "i");
const committedPasswordRegex = new RegExp("INSTAGRAM_" + "PASSWORD=.+", "i");

const forbiddenPatterns = [
  { label: "private n8n cloud URL", regex: /https?:\/\/[^"'\s]+\.app\.n8n\.cloud/i },
  { label: "private Google Sheet URL", regex: /docs\.google\.com\/spreadsheets\/d\/[A-Za-z0-9_-]{20,}/i },
  { label: "exported credential binding", regex: /"credentials"\s*:/i },
  { label: "exported webhook ID", regex: /"webhookId"\s*:/i },
  { label: "legacy private target", regex: legacyTargetRegex },
  { label: "mojibake text", regex: /[\u00f0\u0178\u00e2\u0161\u00ef\u00b8]/ },
  { label: "committed password value", regex: committedPasswordRegex }
];

for (const filePath of listFiles(root).filter(isTextFile)) {
  const relativePath = path.relative(root, filePath).replace(/\\/g, "/");
  const content = fs.readFileSync(filePath, "utf8");

  for (const { label, regex } of forbiddenPatterns) {
    if (regex.test(content)) {
      fail(`${relativePath} contains ${label}.`);
    }
  }
}

if (failures.length > 0) {
  console.error("Project validation failed:");
  for (const failure of failures) {
    console.error(`- ${failure}`);
  }
  process.exit(1);
}

console.log("Project validation passed.");
