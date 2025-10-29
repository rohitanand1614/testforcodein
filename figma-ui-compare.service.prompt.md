---
name: "Figma ↔ UI Comparison"
description: "Compare a Figma component (and its children) with its implementation on a live site using Figma MCP + Playwright MCP."
mode: "agent"
---

# Behavior
When invoked, always follow these fixed steps unless overridden:

**Step 1: Use Figma MCP**
- Call: `get_design_context(fileUrl={figmaUrl})`
- Store as `figmaDesign`
- Ensure `figmaDesign` includes:
  - Parent component styles  
  - All child elements with: fontFamily, fontSize, color, backgroundColor, spacing  
  - Text content for each textual element  

**Step 2: Use Playwright MCP**
- Navigate to `{siteUrl}` in headed mode  
- Locate parent element using `{selectorType}={selector}`  
- For each child element:
  - Extract computed styles: fontFamily, fontSize, color, backgroundColor  
  - Extract text content  
  - Map each child to its corresponding Figma child by name or hierarchy  

**Step 3: Compare**
- For every mapped child element:
  - Compare fontFamily, fontSize, color, backgroundColor between Figma and UI  
  - Include text content comparison for clarity  
- Print a summarized table with columns: **Text | Figma Styles | UI Styles | Status**

# Expected Inputs
| Name | Type | Example |
|------|------|----------|
| figmaUrl | string | https://www.figma.com/design/abc123?node-id=7512-6567&m=dev |
| siteUrl | string | https://example.com/home |
| selectorType | string | class / id / css |
| selector | string | hero-wrapper |

# Usage Hints
If the user provides only URLs and selector details, infer defaults for missing fields (e.g. `selectorType="class"` if not specified).

Respond only with:
1. Summary of actions (one sentence)
2. The generated comparison plan (markdown list)
3. (Optional) the code snippet or MCP commands to execute comparison
