# Agency Intake - questions Claude walks you through

Claude asks these, you answer, and the answers populate `scripts/values.json` -> auto-filled into
your GHL custom values by `setup_values.py`. Some answers you have up front; a few are generated
while you build (survey, contract, agents) and filled in on a second pass.

## A. Up front (answer these first)
| Question | Fills custom value | Example |
|---|---|---|
| What's your agency / business name? | `your_business_name` | Summit AI |
| Who's the sender on emails (name)? | `your_name` | Dan at Summit AI |
| Sender email? | `your_email` | dan@summitai.com |
| What should the AI call itself? | `ai_assistant_name` | Maya |
| One-time setup / build fee? | `setup_fee` | $1,000 |
| Monthly retainer? | `monthly_retainer` | $1,200 |
| Your demo FAQ for the AI (what it should know to answer prospects) | `frequently_asked_questions` | (paste your FAQ) |

## B. Generated during setup (fill on the second pass)
| Question | Fills custom value | Where it comes from |
|---|---|---|
| Your Leadlock API key | `leadlock_api_key` | Leadlock -> Settings -> API key |
| Your demo agent's ID | `leadlock_agent_id` | the Leadlock agent that runs the demo + books |
| Your reminder/follow-up agent's ID | `leadlock_reminder_agent_id` | the Leadlock follow-up agent |
| Your Client Intake survey share link | `intake_form_link` | after you build the intake survey (GHL Surveys) |
| Your service agreement doc link | `agreement_link` | after you build + publish the contract (Documents & Contracts) |
| Your voice orb page link | `orb_link` | after you create the orb demo in Leadlock |

### Optional branding (in the snapshot, brands the funnel + orb pages - skip to leave default)
| Question | Fills custom value |
|---|---|
| Logo URL | `logo` |
| Primary brand color (hex) | `primary_color` |
| Secondary brand color (hex) | `secondary_color` |
| Orb "thank you" page link | `orb_thank_you_page_link` |

## C. Script credentials -> go in `.env` (NOT values.json)
These authenticate the scripts to GHL. Put them in the kit's `.env` file:
| Env var | Value |
|---|---|
| `GHL_LOCATION_ID` | your GHL sub-account Location ID (the long string in the GHL URL) |
| `GHL_PIT` | a GHL Private Integration Token. Create at Settings -> Private Integrations with the `customValues` read + write scopes. Starts with `pit-`. |

## How it flows
1. Claude asks Section A -> writes `scripts/values.json`; Section C creds go in the kit's `.env`.
2. Run `setup_values.py` -> fills the up-front values; the Section B ones show as "not filled yet".
3. You build the survey, contract, agents, orb (per `setup-checklist.md`), collect those links/IDs.
4. Claude updates `values.json` with Section B -> re-run `setup_values.py` -> everything filled.
5. Run `verify.py` -> confirms no gaps.
