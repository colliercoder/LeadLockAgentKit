# Leadlock API Reference

Base URL: https://leadlock-app.onrender.com
Auth: Bearer token (JWT) in Authorization header, OR X-API-Key header. Both are accepted.
OpenAPI Version: 3.1.0
API Version: 0.1.0

---

## Account

### GET /account/delete-request
Get Deletion Request Status

Return the most recent deletion request status for this tenant, or null.

**Responses:**
- `200`: Successful Response

---

### POST /account/delete-request
Request Account Deletion

Submit a GDPR/CCPA account deletion request.

Only the account owner (not sub-account users) may request deletion.
The request is captured and Leadlock is notified; Leadlock processes within
the GDPR (1 month) / CCPA (45 days) SLA whichever is shorter.

**Request Body:** `DeletionRequestPayload` (application/json)
- reason: string | null

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Admin

### DELETE /admin/agencies/{agency_id}
Delete Agency Endpoint

Soft-delete an agency and cascade through sub-accounts (super admin only).

**Parameters:**
- `agency_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /admin/dashboard
Get Admin Dashboard

Get aggregated admin dashboard metrics from all external sources.

**Responses:**
- `200`: Successful Response
  Returns: `AdminDashboardResponse`

---

### GET /admin/issues
List Issues

List all issue reports (super admin only).

**Parameters:**
- `resolved` (query, boolean | null) — Filter by resolved status

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /admin/issues/{issue_id}
Resolve Issue

Resolve or unresolve an issue report.

**Parameters:**
- `issue_id` (path, string (required))

**Request Body:** `IssueResolveRequest` (application/json)
- resolved: boolean (required)

**Responses:**
- `200`: Successful Response
  Returns: `IssueReportResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /admin/rate-limits
Get Rate Limit Status

Get current voice API rate limit utilization per provider.

**Responses:**
- `200`: Successful Response

---

### POST /admin/rate-limits/check
Trigger Quota Check

Manually trigger a provider quota check (runs the scheduled job now).

**Responses:**
- `200`: Successful Response

---

### GET /admin/users
List Users

Get paginated list of users with analytics metrics.

**Parameters:**
- `page` (query, integer) — Page number
- `per_page` (query, integer) — Items per page
- `search` (query, string | null) — Search by email or name
- `sort_by` (query, string enum ['last_login', 'email', 'health_score', 'production_minutes', 'logins_30d', 'created_at']) — Sort field
- `sort_order` (query, string enum ['asc', 'desc']) — Sort order
- `plan` (query, string | null) — Filter by plan
- `status` (query, string enum ['healthy', 'warning', 'at_risk'] | null) — Filter by health status

**Responses:**
- `200`: Successful Response
  Returns: `PaginatedUsersResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /admin/users/analytics
Get User Analytics

Get aggregate user analytics (KPIs, charts, churn risk).

**Responses:**
- `200`: Successful Response
  Returns: `UserAnalyticsAggregates`

---

### POST /admin/users/create
Create User

Create a new user with email/password (super admin only).

**Request Body:** `CreateUserRequest` (application/json)
- email: string (required)
- password: string (required)
- plan: string enum ['starter', 'pro', 'agency']
- company_name: string | null

**Responses:**
- `200`: Successful Response
  Returns: `CreateUserResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /admin/users/{user_id}
Get User Detail

Get detailed user information with full analytics.

**Parameters:**
- `user_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `UserDetailResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /admin/users/{user_id}/status
Update User Status

Enable or disable a user account (super admin only).

**Parameters:**
- `user_id` (path, string (required))

**Request Body:** `UpdateUserStatusRequest` (application/json)
- disabled: boolean (required)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /admin/voice/model-adoption
Get Voice Model Adoption

Count OpenAI voice agents grouped by openai_voice_model.

Used to inform the Phase 2 backfill decision — when v2 adoption is
meaningful, support can switch from manual sub-attach to auto-attach on
signup.

**Responses:**
- `200`: Successful Response

---

## Affiliates

### GET /affiliates/code
Get Affiliate Code

Get current user's affiliate code.

Creates a new code if one doesn't exist yet.
Returns the code and full referral URL.

**Responses:**
- `200`: Successful Response
  Returns: `AffiliateCodeResponse`

---

### GET /affiliates/stats
Get Affiliate Stats

Get affiliate dashboard stats.

Returns total referrals, earnings, and list of all commissions.

**Responses:**
- `200`: Successful Response
  Returns: `AffiliateStatsResponse`

---

## Agency

### GET /agency/agents
List All Sub Account Agents

List all agents across ALL sub-accounts.

Used by agencies to view, filter, and manage agents across their entire portfolio.
Returns agents enriched with sub-account name and phone count.

**Responses:**
- `200`: Successful Response
  Returns: `AllSubAccountAgentsResponse`

---

### POST /agency/agents/{agent_id}/copy
Copy Agent Between Sub Accounts

Copy an agent from one sub-account to another (agency-only).

Verifies the agency owns both source and target sub-accounts.
Creates a disabled copy with " (Copy)" suffix.

Note: Returns the raw agent dict from the database insert, not AgentResponse.
AgentResponse has computed fields (phone_count, text_assistants) that aren't
present in the raw insert result. The frontend doesn't use this response body
for rendering — it invalidates the query cache after a successful copy.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `CopyAgentToSubAccountRequest` (application/json)
- source_tenant_id: string (required)
- target_tenant_id: string (required)

**Responses:**
- `201`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agency/branding
Get Branding

Get branding settings.

Works for both agencies (own settings) and sub-accounts (parent settings).

**Responses:**
- `200`: Successful Response
  Returns: `BrandingSettings`

---

### PATCH /agency/branding
Update Branding

Update branding settings.

Only agencies can update branding.

**Request Body:** `UpdateBrandingRequest` (application/json)
- company_name: string | null
- primary_color: string | null
- support_email: string | null
- support_url: string | null

**Responses:**
- `200`: Successful Response
  Returns: `BrandingSettings`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agency/branding/favicon
Upload Favicon

Upload a favicon image.

Accepts PNG, JPEG, SVG, or ICO. Maximum 5MB.

**Responses:**
- `200`: Successful Response
  Returns: `LogoUploadResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agency/branding/favicon
Delete Favicon

Delete the favicon image and clear favicon_url. Returns refreshed branding.

**Responses:**
- `200`: Successful Response
  Returns: `BrandingSettings`

---

### POST /agency/branding/logo
Upload Logo

Upload a logo image.

Accepts PNG, JPEG, SVG, or ICO. Maximum 5MB.

**Responses:**
- `200`: Successful Response
  Returns: `LogoUploadResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agency/branding/logo
Delete Logo

Delete the logo image and clear logo_url. Returns refreshed branding.

**Responses:**
- `200`: Successful Response
  Returns: `BrandingSettings`

---

### GET /agency/functions
List All Sub Account Functions

List all custom functions across ALL sub-accounts.

Used by agencies to select a function to copy/share to another sub-account.
Returns functions with their source sub-account info.

**Responses:**
- `200`: Successful Response
  Returns: `AllSubAccountFunctionsResponse`

---

### GET /agency/integrations
List Agency Integrations

List ALL integrations owned by the agency (GHL, Twilio).

Returns integrations available for assignment to sub-accounts.

**Responses:**
- `200`: Successful Response
  Returns: `AgencyIntegrationsResponse`

---

### GET /agency/invoice-summary
Get Invoice Summary

Get per-sub-account invoice summary for the current billing period.

Returns voice minutes + revenue, text count + revenue, platform fees,
and total due for every active sub-account. Sorted by total due descending.

**Responses:**
- `200`: Successful Response
  Returns: `InvoiceSummaryResponse`

---

### GET /agency/my-integration
Get My Integration Legacy

Legacy endpoint - redirects to /my-integrations.

Kept for backward compatibility.

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountIntegrationsResponse`

---

### GET /agency/my-integrations
Get My Integrations

Get all integrations assigned to the current sub-account.

Returns integrations assigned by the parent agency.

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountIntegrationsResponse`

---

### GET /agency/overview
Get Agency Overview

Get agency dashboard overview stats.

Includes aggregated metrics across all sub-accounts.

**Responses:**
- `200`: Successful Response
  Returns: `AgencyOverview`

---

### GET /agency/sub-accounts
List Sub Accounts

List all sub-accounts for the agency.

Returns sub-accounts with billing info and usage stats.

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountListResponse`

---

### POST /agency/sub-accounts
Create Sub Account

Create a new sub-account.

Validates:
- Agency has not exceeded sub_account_limit
- Slug is globally unique

**Request Body:** `CreateSubAccountRequest` (application/json)
- name: string (required)
- slug: string (required)
- admin_email: string | null
- admin_name: string | null
- per_minute_rate_cents: integer
- monthly_platform_fee_cents: integer
- billing_start_day: integer
- upcharge_by_provider: object | null
- test_demo_upcharge_by_provider: object | null
- text_upcharge_by_type: object | null

**Responses:**
- `201`: Successful Response
  Returns: `SubAccountResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agency/sub-accounts/check-slug
Check Slug Availability

Check if a slug is available for use.

Returns availability status without creating anything.
Useful for real-time validation in the UI.

**Request Body:** `CheckSlugRequest` (application/json)
- slug: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `CheckSlugResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agency/sub-accounts/{sub_account_id}
Get Sub Account

Get a single sub-account with full details.

**Parameters:**
- `sub_account_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /agency/sub-accounts/{sub_account_id}
Update Sub Account

Update a sub-account's settings.

**Parameters:**
- `sub_account_id` (path, string (required))

**Request Body:** `UpdateSubAccountRequest` (application/json)
- name: string | null
- admin_email: string | null
- admin_name: string | null
- per_minute_rate_cents: integer | null
- monthly_platform_fee_cents: integer | null
- is_active: boolean | null
- billing_start_day: integer | null
- upcharge_by_provider: object | null
- test_demo_upcharge_by_provider: object | null
- text_upcharge_by_type: object | null

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agency/sub-accounts/{sub_account_id}
Delete Sub Account

Soft-delete a sub-account (sets is_active=False).

Historical data is preserved.

**Parameters:**
- `sub_account_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agency/sub-accounts/{sub_account_id}/integrations
Assign Integrations To Sub Account

Assign multiple integrations to a sub-account.

Rules:
- Maximum 1 GHL integration per sub-account
- Multiple Twilio/other integrations allowed
- All integrations must belong to the parent agency

**Parameters:**
- `sub_account_id` (path, string (required))

**Request Body:** `AssignIntegrationsRequest` (application/json)
- integration_ids: array of string (required)

**Responses:**
- `200`: Successful Response
  Returns: `AssignIntegrationsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agency/sub-accounts/{sub_account_id}/integrations
Remove All Integrations From Sub Account

Remove ALL integration assignments from a sub-account.

**Parameters:**
- `sub_account_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agency/sub-accounts/{sub_account_id}/integrations/{integration_id}
Remove Integration From Sub Account

Remove a specific integration from a sub-account.

**Parameters:**
- `sub_account_id` (path, string (required))
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `RemoveIntegrationResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agency/sub-accounts/{sub_account_id}/invite
Send Sub Account Invite

Send an invitation email to the sub-account admin.

**Parameters:**
- `sub_account_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agency/sub-accounts/{sub_account_id}/usage
Get Sub Account Usage

Get usage records for a specific sub-account.

**Parameters:**
- `sub_account_id` (path, string (required))
- `date_from` (query, string | null)
- `date_to` (query, string | null)
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `UsageExportResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agency/usage
Get All Usage

Get usage records across all sub-accounts.

**Parameters:**
- `date_from` (query, string | null)
- `date_to` (query, string | null)
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `UsageExportResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agency/usage/export
Export Usage Csv

Export usage data as CSV.

Returns a streaming response to handle large datasets efficiently.

**Parameters:**
- `sub_account_id` (query, string | null)
- `date_from` (query, string | null)
- `date_to` (query, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Agents

### GET /agents
List Agents

List all agents for the current tenant.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: returns their agents.

**Responses:**
- `200`: Successful Response
  Returns: `AgentListResponse`

---

### POST /agents
Create Agent

Create a new agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: creates agent under their tenant.
Checks agent limit for the effective tenant.

**Request Body:** `AgentCreate` (application/json)
- name: string (required)
- system_prompt: string (required)
- greeting: string | null
- greeting_outbound: string | null
- voice: string
- temperature: number
- business_name: string | null
- industry: string | null
- ghl_phone_number: string | null
- calendar_provider: string | null — Calendar provider: 'gohighlevel'
- calendar_integration_id: string | null — Which GHL integration to use (for multi-account support)
- calendar_id: string | null — Calendar ID from provider
- tools_enabled: array of string | null — List of enabled tool names (e.g., ['end_call', 'book_appointment'])
- timezone: string — IANA timezone (e.g., America/New_York, America/Los_Angeles)
- vad_threshold: number — VAD sensitivity (0.0-1.0, higher = less sensitive)
- vad_silence_duration_ms: integer — Silence duration before ending turn (ms)
- vad_prefix_padding_ms: integer — Audio capture before speech detection (ms)
- enable_web_search: boolean — Enable web search capability
- enable_x_search: boolean — Enable X (Twitter) search
- x_search_handles: array of string | null — Allowed X handles for search (e.g., ['elonmusk', 'xai'])
- enable_collections_search: boolean — Enable document search from tenant knowledge base
- knowledge_base_ids: array of string — Knowledge Base IDs this agent can search (when enable_collections_search=true)
- enable_recording_disclosure: boolean — Announce call recording at start of calls (required for two-party consent states)
- recording_enabled: boolean — When true, defer GHL conversation sync and post-call webhook to recording.ready so the Twilio recording URL is included.
- enable_contact_intelligence: boolean — Fetch caller context (GHL contact + call history) before answering
- ai_speaks_first: boolean — If true, AI greets caller immediately. If false, AI waits for caller to speak first.
- ai_speaks_first_outbound: boolean — If true, AI greets recipient immediately on outbound calls.
- finish_greeting_before_listening: boolean — If true, caller cannot interrupt the agent's first response (inbound). Ignored if ai_speaks_first is false — validator w
- finish_greeting_before_listening_outbound: boolean — If true, recipient cannot interrupt the agent's first response on outbound calls. Ignored if ai_speaks_first_outbound is
- prompt_includes_contact_intelligence: boolean — True if prompt includes Caller Intelligence section for using pre-call context
- voice_provider: string — Voice provider: 'xai' (Grok), 'elevenlabs' (ElevenLabs), 'openai' (OpenAI), or 'gemini' (Gemini)
- gemini_voice: string — Gemini prebuilt voice name (30 options)
- gemini_start_sensitivity: string — Gemini start-of-speech sensitivity: low (ignores noise) or high (reacts to everything)
- gemini_end_sensitivity: string — Gemini end-of-speech sensitivity: low (patient, waits for clear silence) or high (quick cutoff). WARNING: LOW on 8kHz te
- gemini_thinking_level: string — Gemini 3.1 thinking level: none (off, fastest), minimal (very light), low (basic reasoning), medium, high (most thorough
- gemini_language_code: string | null — BCP-47 language code hint for Gemini speech (e.g., 'en-US', 'es-US', 'fr-FR'). None = auto-detect.
- gemini_affective_dialog: boolean — Enable emotion/tone awareness in Gemini responses (Preview feature)
- gemini_proactive_audio: boolean — Allow Gemini to stay silent when no clear request is made (Preview feature)
- gemini_top_k: integer | null — Gemini top-K sampling: number of top tokens considered (1-100, None=model default)
- gemini_top_p: number | null — Gemini top-P nucleus sampling threshold (0.0-1.0, None=model default)
- openai_voice: string — OpenAI voice ID. v1.5 voices: alloy, ash, ballad, coral, echo, sage, shimmer, verse. v2 adds: marin, cedar (only availab
- openai_vad_type: string — OpenAI VAD type: semantic_vad (AI-based) or server_vad (volume-based)
- openai_vad_eagerness: string — OpenAI semantic VAD eagerness: low (patient) to high (responsive)
- openai_noise_reduction: string — OpenAI noise reduction: far_field (phone), near_field (mic), or disabled
- openai_voice_model: string — OpenAI Realtime model version. v1.5 is the default audio model; v2 adds reasoning at premium pricing.
- openai_reasoning_effort: string — Reasoning effort for gpt-realtime-2. Ignored on v1.5. Default 'low' is recommended for production voice.
- elevenlabs_voice_id: string | null — ElevenLabs voice ID
- elevenlabs_model_id: string — LLM model ID for ElevenLabs agent (e.g., claude-sonnet-4-5, gpt-4o-mini, claude-3-haiku)
- elevenlabs_speed: number — Speaking speed for ElevenLabs (0.7-1.2x)
- elevenlabs_eagerness: string — Turn-taking eagerness for ElevenLabs: 'low', 'normal', or 'high'
- elevenlabs_language: string — Language code for ElevenLabs agent (e.g., 'en', 'es', 'fr')
- elevenlabs_additional_languages: array of string — Additional language codes for multilingual support (e.g., ['es', 'fr'])
- elevenlabs_stability: number — Voice stability for ElevenLabs (0.0=creative, 0.5=natural, 1.0=robust)
- elevenlabs_max_duration_seconds: integer | null — Max call duration in seconds for ElevenLabs (None=unlimited, min 60)
- elevenlabs_emotion_tags: array of object | null — Custom emotion tags for ElevenLabs: [{name, description}]
- elevenlabs_tool_call_sound: string | null — Sound played during ElevenLabs tool execution: typing, elevator1-4, none
- elevenlabs_pre_tool_speech: boolean | null — Agent announces action before executing slow tools (ElevenLabs only)
- xai_audio_tags: array of string | null — xAI audio delivery tags: ['[breath]', '[pause]', '<whisper>', ...]
- agent_mode: string — How this agent handles calls: 'inbound', 'outbound', or 'both'
- voice_enabled: boolean — Enable voice/phone channel
- text_enabled: boolean — Enable text/SMS channel
- amd_enabled: boolean — Enable Twilio AMD for outbound calls ($0.01/call)
- amd_voicemail_behavior: string — Action when voicemail detected: hangup, static_message, dynamic_message, agent_decides
- amd_voicemail_message: string | null — Message to leave on voicemail (supports {{variables}} for dynamic_message)
- amd_voicemail_audio_url: string | null — Audio file URL to play as voicemail (alternative to TTS)
- transfer_targets: array of object | null — Transfer targets: [{name, number, reason}]
- whisper_enabled: boolean — Enable AI-generated whisper summary when transferring calls
- ghl_tags: array of object | null — Available tags for GHL add_tag/remove_tag: [{name}]
- ghl_remove_tags: array of object | null — Tag rules for remove_tag: [{name, condition?}]
- ghl_workflows: array of object | null — Available workflows for GHL trigger_workflow: [{id, name, description?}]
- ghl_pipelines: array of object | null — Available pipelines for GHL opportunities: [{id, name, stages: [{id, name}]}]
- sms_templates: array of object | null — SMS templates for send_sms: [{name, content}]
- sms_phone_number_id: string | null — Phone number ID to use for send_sms tool (overrides agent's voice number)
- max_call_duration_minutes: integer — Max call duration in minutes (0=unlimited, max 180)
- max_silence_seconds: integer — Max silence before ending call in seconds (0=unlimited, max 600)
- calendar_configs: array of object | null — Calendar configurations: [{calendar_id, integration_id, label, provider}]
- multi_calendar_behavior: string — Multi-calendar behavior: 'ask_user' (present options) or 'auto_first' (book first available)
- variable_definitions: array of VariableDefinition | null — Template variables for prompt substitution: [{name, description?, required?, default_value?}]
- tool_instructions: object | null — Per-tool usage instructions: {"tool_name": "instruction text"}
- text_model: string — LLM model for text assistant (claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-sonnet-4-5-20250929, claude-opus-4-6,
- channel_pivot_enabled: boolean — Auto-send text when outbound call fails (no-answer, busy, voicemail)
- mcp_servers: array of MCPServerConfig | null

**Responses:**
- `201`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/share-links
List Share Links

List all active share links for the current tenant.

**Responses:**
- `200`: Successful Response

---

### POST /agents/test/chat
Test Agent Chat

Test agent in text mode.

Uses xAI Chat Completions API with same Grok model as voice testing.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: tests their agent.

**Request Body:** `TestChatRequest` (application/json)
- agent_id: string (required) — Agent ID to test
- messages: array of ChatMessage (required) — Conversation history including new user message

**Responses:**
- `200`: Successful Response
  Returns: `TestChatResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/test/voice
Test Agent Voice

Test agent in voice mode.

Uses xAI Realtime Voice API to process audio and return AI response.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: tests their agent.

**Request Body:** `TestVoiceRequest` (application/json)
- agent_id: string (required) — Agent ID to test
- audio_base64: string (required) — Base64-encoded PCM16 audio at 24kHz

**Responses:**
- `200`: Successful Response
  Returns: `TestVoiceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/wizard/defaults
Get Wizard Defaults

Get default settings for the agent wizard.

Returns recommended settings for a receptionist agent.

**Responses:**
- `200`: Successful Response

---

### POST /agents/wizard/enhance-description
Enhance Description

Enhance a basic business description using AI.

Takes a rough description and makes it more polished and professional
while keeping it concise (under 50 words).

**Request Body:** `EnhanceDescriptionRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- description: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `EnhanceDescriptionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/generate-all-knowledge
Generate All Knowledge Endpoint

Generate all knowledge sections at once.

This is a convenience endpoint that generates services, pricing,
team, and FAQs in a single call. Takes longer but provides
everything needed for the agent prompt.

**Request Body:** `app__agents__prompt_router__GenerateAllKnowledgeRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- description: string — Business description for context
- agent_mode: string — Agent mode — outbound routes 'team' to objections generator

**Responses:**
- `200`: Successful Response
  Returns: `GenerateAllKnowledgeResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/generate-expressive
Generate Expressive Endpoint

Generate expressive voice configuration using AI.

Analyzes the agent's prompt and user preferences to generate:
- Audio tags for ElevenLabs v3 expressive mode
- Custom emotion tags with descriptions
- A prompt section with tone/delivery guidance
- The full updated prompt with the section merged in

Supports presets, custom descriptions, and iterative refinement.

**Request Body:** `GenerateExpressiveRequest` (application/json)
- current_prompt: string (required) — The existing system prompt for context
- preset: string | null — Preset style: empathetic_support, high_energy_sales, professional_service, friendly_fun
- custom_description: string | null — Free-text description of desired emotional delivery
- refinement: string | null — Refinement instruction for a previous result
- previous_result: object | null — Previous AI output to refine

**Responses:**
- `200`: Successful Response
  Returns: `GenerateExpressiveResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/generate-function-schema
Generate Function Schema Endpoint

Generate a custom function schema using AI.

Takes a plain English description and generates:
- Function name (snake_case)
- Description for the AI to understand when to use it
- JSON Schema for parameters
- Recommended HTTP method (GET/POST)

**Example:**
```json
{
  "description": "Capture lead info: name, email, phone number"
}
```

Returns a complete function definition ready for the custom function form.

**Request Body:** `GenerateFunctionSchemaRequest` (application/json)
- description: string (required) — Plain English description of what the function should do
- webhook_purpose: string | null — Optional context about where the webhook sends data

**Responses:**
- `200`: Successful Response
  Returns: `GenerateFunctionSchemaResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/generate-knowledge
Generate Knowledge

Generate AI suggestions for a specific knowledge section.

This endpoint uses xAI to generate content for one section at a time,
allowing users to iterate on each section individually.

**Sections:**
- `services`: Products and services offered
- `pricing`: Pricing information
- `team`: Team members and roles
- `faqs`: Common questions and answers

**Request Body:** `app__agents__prompt_router__GenerateKnowledgeRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- section: string (required) — Section to generate: services, pricing, team, or faqs
- description: string — Business description for context
- services: string — Existing services list (for pricing/faqs context)
- agent_mode: string — Agent mode — outbound routes 'team' to objections generator

**Responses:**
- `200`: Successful Response
  Returns: `GenerateKnowledgeResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/import-website
Import From Website

Import business information from a website.

This endpoint:
1. Scrapes the provided URL and discovers internal pages
2. Scrapes up to 8 key pages (about, services, pricing, team, faq)
3. Uses AI to extract business information from the combined content
4. Returns structured data ready for the wizard form

**Request Body:** `ImportWebsiteRequest` (application/json)
- url: string (required) — Website URL to scrape (e.g., https://example.com)

**Responses:**
- `200`: Successful Response
  Returns: `ImportWebsiteResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/wizard/import-website-stream
Import From Website Stream

Import business information from a website with real-time progress streaming.

Returns Server-Sent Events with progress updates:
- progress: {step, current, total, detail}
- result: {business_name, industry, ...}
- error: {message}

**Parameters:**
- `url` (query, string (required)) — Website URL to scrape

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/wizard/industry-presets
Get Industry Presets

Get available industry presets.

Returns a list of supported industries and their associated
suggestions for services and FAQs.

**Responses:**
- `200`: Successful Response
  Returns: `IndustryPresetsResponse`

---

### POST /agents/wizard/preview-greeting-tts
Preview Greeting Tts

Generate a TTS audio preview of a greeting message.

Calls the appropriate TTS provider API and streams back MP3 audio.
xAI falls back to OpenAI TTS with voice "alloy" (no REST TTS available).

**Request Body:** `PreviewGreetingTTSRequest` (application/json)
- text: string (required)
- voice_provider: string (required)
- voice_id: string (required)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/preview-prompt
Preview Prompt

Preview the full generated prompt before creating the agent.

This builds the complete receptionist prompt from the provided
knowledge sections and returns it along with recommended settings.

**Request Body:** `PreviewPromptRequest` (application/json)
- business_name: string (required)
- agent_name: string
- industry: string
- personality: string
- description: string
- services: string
- pricing: string
- team: string
- faqs: string
- product_offer: string
- qualification_criteria: string
- common_objections: string
- voice_provider: string
- agent_type: string | null
- sales_methodology: string | null
- cta_type: string | null

**Responses:**
- `200`: Successful Response
  Returns: `PreviewPromptResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/suggest-functions
Suggest Functions Endpoint

Get AI-powered function/tool suggestions for an agent.

Analyzes industry, agent mode, and business description to recommend
which tools to enable, with a reason for each suggestion.

**Request Body:** `SuggestFunctionsRequest` (application/json)
- industry: string (required) — Business industry
- agent_mode: string — Agent mode: inbound, outbound, or both
- description: string — Business description for context
- has_ghl: boolean — Whether GoHighLevel CRM is connected
- system_prompt: string | null — Existing system prompt for deeper context

**Responses:**
- `200`: Successful Response
  Returns: `SuggestFunctionsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/update-prompt
Update Prompt Endpoint

Update an existing system prompt using AI.

Makes surgical modifications to the prompt based on the instruction,
preserving the overall structure while adding/modifying specific parts.

**Features:**
- Preserves prompt structure
- Converts negative instructions to positive framing
- Adds anti-patterns to dedicated section
- Optional: integrate custom functions documentation

**Example:**
```json
{
  "current_prompt": "You are a helpful assistant...",
  "instruction": "Add FAQ about return policy"
}
```

**Request Body:** `UpdatePromptRequest` (application/json)
- current_prompt: string (required) — The existing system prompt to modify
- instruction: string (required) — Instructions for how to modify the prompt
- functions: array of FunctionForUpdate — Optional: custom functions to integrate into the prompt
- quick_action: string enum ['integrate_functions', 'condense'] | null — Special action: 'integrate_functions' or 'condense'

**Responses:**
- `200`: Successful Response
  Returns: `UpdatePromptResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/wizard/update-prompt-contact-intelligence
Update Prompt Contact Intelligence Endpoint

Update a system prompt to add or remove Contact Intelligence instructions.

This endpoint helps users configure their agent prompts to leverage
caller context data (name, company, previous calls, tags, etc.).

**Actions:**
- `add`: Injects a "## Caller Intelligence" section and updates greeting
- `remove`: Removes the CI section and reverts greeting to generic

**Example:**
```json
{
  "current_prompt": "You are a helpful assistant...",
  "action": "add"
}
```

**Request Body:** `ContactIntelligencePromptRequest` (application/json)
- current_prompt: string (required) — The existing system prompt to modify
- action: string (required) — Action to perform: 'add' to inject CI section, 'remove' to strip it

**Responses:**
- `200`: Successful Response
  Returns: `UpdatePromptResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/{agent_id}
Get Agent

Get a specific agent by ID.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: returns their agent.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /agents/{agent_id}
Update Agent

Update an agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: updates their agent.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `AgentUpdate` (application/json)
- name: string | null
- system_prompt: string | null
- greeting: string | null
- greeting_outbound: string | null
- voice: string | null
- temperature: number | null
- is_active: boolean | null
- business_name: string | null
- industry: string | null
- ghl_phone_number: string | null
- calendar_provider: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- tools_enabled: array of string | null
- timezone: string | null
- vad_threshold: number | null
- vad_silence_duration_ms: integer | null
- vad_prefix_padding_ms: integer | null
- enable_web_search: boolean | null
- enable_x_search: boolean | null
- x_search_handles: array of string | null
- enable_collections_search: boolean | null
- knowledge_base_ids: array of string | null
- enable_recording_disclosure: boolean | null
- recording_enabled: boolean | null
- enable_contact_intelligence: boolean | null
- ai_speaks_first: boolean | null
- ai_speaks_first_outbound: boolean | null
- finish_greeting_before_listening: boolean | null
- finish_greeting_before_listening_outbound: boolean | null
- prompt_includes_contact_intelligence: boolean | null
- voice_provider: string | null — Voice provider: 'xai' (Grok), 'elevenlabs' (ElevenLabs), 'openai' (OpenAI), or 'gemini' (Gemini)
- gemini_voice: string | null
- gemini_start_sensitivity: string | null
- gemini_end_sensitivity: string | null
- gemini_thinking_level: string | null
- gemini_language_code: string | null
- gemini_affective_dialog: boolean | null
- gemini_proactive_audio: boolean | null
- gemini_top_k: integer | null
- gemini_top_p: number | null
- openai_voice: string | null
- openai_vad_type: string | null
- openai_vad_eagerness: string | null
- openai_noise_reduction: string | null
- openai_voice_model: string | null
- openai_reasoning_effort: string | null
- elevenlabs_voice_id: string | null
- elevenlabs_model_id: string | null
- elevenlabs_speed: number | null
- elevenlabs_eagerness: string | null
- elevenlabs_language: string | null
- elevenlabs_additional_languages: array of string | null
- elevenlabs_stability: number | null
- elevenlabs_max_duration_seconds: integer | null
- elevenlabs_emotion_tags: array of object | null
- elevenlabs_tool_call_sound: string | null
- elevenlabs_pre_tool_speech: boolean | null
- xai_audio_tags: array of string | null
- agent_mode: string | null — How this agent handles calls
- voice_enabled: boolean | null
- text_enabled: boolean | null
- amd_enabled: boolean | null
- amd_voicemail_behavior: string | null
- amd_voicemail_message: string | null
- amd_voicemail_audio_url: string | null
- transfer_targets: array of object | null
- whisper_enabled: boolean | null
- ghl_tags: array of object | null
- ghl_remove_tags: array of object | null
- ghl_workflows: array of object | null
- ghl_pipelines: array of object | null
- sms_templates: array of object | null
- sms_phone_number_id: string | null
- max_call_duration_minutes: integer | null
- max_silence_seconds: integer | null
- calendar_configs: array of object | null
- multi_calendar_behavior: string | null
- variable_definitions: array of VariableDefinition | null
- tool_instructions: object | null
- text_model: string | null
- channel_pivot_enabled: boolean | null
- mcp_servers: array of MCPServerConfig | null

**Responses:**
- `200`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agents/{agent_id}
Delete Agent

Delete an agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: deletes their agent.

Raises ValidationError if agent is linked to text assistants.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/copy-to/{target_tenant_id}
Copy Agent To Sub Account

Copy an agent to another sub-account (agency-only).

Verifies the user's agency owns both source and target sub-accounts.
Clears tenant-specific fields (calendars, knowledge bases).

**Parameters:**
- `agent_id` (path, string (required))
- `target_tenant_id` (path, string (required))

**Responses:**
- `201`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/duplicate
Duplicate Agent

Duplicate an agent within the same tenant.

Creates a copy with " (Copy)" appended to name and is_active=False.
ElevenLabs agent is re-synced if applicable.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `201`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/{agent_id}/functions
List Agent Functions

List functions attached to an agent plus available library functions.

Returns two lists:
- attached: Functions currently attached to this agent
- available: Library functions not yet attached

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `AgentFunctionsListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/functions
Create Custom Function

Create a new custom function and attach it to this agent.

Backward-compatible endpoint that creates in library and auto-attaches.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `CustomFunctionCreate` (application/json)
- name: string (required) — Function name in snake_case (e.g., check_inventory)
- description: string (required) — Description of what the function does (shown to AI)
- parameters: object — JSON Schema for function parameters
- webhook_url: string (required) — Webhook URL to call (must start with http:// or https://)
- webhook_method: string — HTTP method for webhook call
- webhook_headers: object — Custom headers to include in webhook request
- webhook_timeout_ms: integer — Timeout for webhook call in milliseconds (1000-30000)
- is_enabled: boolean — Whether the function is enabled
- speak_during_execution: boolean — Whether AI should speak while waiting for webhook response

**Responses:**
- `201`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/functions/attach
Attach Function To Agent

Attach an existing library function to this agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `AttachFunctionRequest` (application/json)
- function_id: string (required) — ID of the function to attach
- is_enabled: boolean — Whether function is enabled for this agent

**Responses:**
- `201`: Successful Response
  Returns: `AttachFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agents/{agent_id}/functions/detach/{function_id}
Detach Function From Agent

Detach a function from this agent.

The function remains in the library and can be re-attached later.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/{agent_id}/functions/{function_id}
Get Custom Function

Get a specific custom function attached to this agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PUT /agents/{agent_id}/functions/{function_id}
Update Custom Function

Update a custom function.

- is_enabled changes only affect this agent
- Other changes affect all agents using this function

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Request Body:** `CustomFunctionUpdate` (application/json)
- name: string | null — Function name in snake_case
- description: string | null — Description of what the function does
- parameters: object | null — JSON Schema for function parameters
- webhook_url: string | null — Webhook URL to call
- webhook_method: string | null — HTTP method for webhook call
- webhook_headers: object | null — Custom headers to include in webhook request
- webhook_timeout_ms: integer | null — Timeout for webhook call in milliseconds
- is_enabled: boolean | null — Whether the function is enabled
- speak_during_execution: boolean | null — Whether AI should speak while waiting for webhook response

**Responses:**
- `200`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agents/{agent_id}/functions/{function_id}
Delete Custom Function

Delete a custom function from the library.

WARNING: This removes the function from ALL agents, not just this one.
Use /detach to remove from only this agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/functions/{function_id}/disable
Disable Function For Agent

Disable a function for this agent.

The function remains attached but won't be used in voice calls.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `AttachFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/functions/{function_id}/enable
Enable Function For Agent

Enable a function for this agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `AttachFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/functions/{function_id}/test
Test Custom Function

Test a custom function by calling its webhook.

Makes a real HTTP request to the webhook URL with test arguments.
Returns timing information and the webhook response.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `agent_id` (path, string (required))
- `function_id` (path, string (required))

**Request Body:** `FunctionTestRequest` (application/json)
- arguments: object — Arguments to pass to the function
- contact_id: string — GHL contact ID — always present via Contact Intelligence

**Responses:**
- `200`: Successful Response
  Returns: `FunctionTestResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/{agent_id}/phone-numbers
Get Agent Phone Numbers

Get phone numbers assigned to an agent.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: returns phone numbers assigned to their agent.

Note: Phone numbers may be owned by an agency (tenant_id = agency) but
assigned to a sub-account (sub_account_id = sub_account). We need to
handle both cases.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /agents/{agent_id}/share
Get Share Link

Get the active share link for an agent.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `CreateShareLinkResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/share
Create Share Link

Create a public share link for an agent.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `CreateShareLinkRequest` (application/json)
- custom_slug: string | null
- expires_in_days: integer | null

**Responses:**
- `200`: Successful Response
  Returns: `CreateShareLinkResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /agents/{agent_id}/share
Revoke Share Link

Revoke (deactivate) the share link for an agent.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /agents/{agent_id}/toggle
Toggle Agent

Toggle an agent's is_active status.

Flips the current is_active value and returns the updated agent.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `AgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Api

### GET /api/public/branding
Get Branding By Domain

Fetch public branding info for a custom domain. No auth required.

**Parameters:**
- `domain` (query, string (required)) — Custom domain to look up branding for

**Responses:**
- `200`: Successful Response
  Returns: `PublicBrandingResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Appointments

### GET /appointments
List Appointments

List GHL calendar appointments for the current tenant.

Returns appointments filtered by date range, calendar, and status.
Cancelled and no-show appointments are excluded by default.

**Parameters:**
- `date_from` (query, string | null) — YYYY-MM-DD, default: today
- `date_to` (query, string | null) — YYYY-MM-DD, default: +30 days
- `calendar_id` (query, string | null) — Filter by calendar ID
- `status` (query, string | null) — Filter by status
- `limit` (query, integer)
- `offset` (query, integer)
- `integration_id` (query, string | null) — Specific GHL integration

**Responses:**
- `200`: Successful Response
  Returns: `AppointmentsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /appointments/contact/{phone}
List Appointments For Contact

List GHL calendar appointments for a specific contact by phone number.

The phone number can be in any format (+15551234567, 555-123-4567, etc.).
Falls back to GHL contact search if phone is not directly on events.

**Parameters:**
- `phone` (path, string (required))
- `date_from` (query, string | null) — YYYY-MM-DD, default: today
- `date_to` (query, string | null) — YYYY-MM-DD, default: +30 days
- `calendar_id` (query, string | null) — Filter by calendar ID
- `status` (query, string | null) — Filter by status
- `limit` (query, integer)
- `offset` (query, integer)
- `integration_id` (query, string | null) — Specific GHL integration

**Responses:**
- `200`: Successful Response
  Returns: `AppointmentsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Auth

### POST /auth/accept-invite
Accept Invite

Accept a sub-account invitation.

Validates token inline and creates auth account if valid.
Returns tokens for immediate login.
Public endpoint - no auth required.
Rate limited: 5 attempts per hour per IP address.

**Request Body:** `AcceptInviteRequest` (application/json)
- token: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)

**Responses:**
- `200`: Successful Response
  Returns: `AuthResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /auth/api-keys
List Api Keys

List all API keys for the current tenant/sub-account.

**Responses:**
- `200`: Successful Response
  Returns: `APIKeyListResponse`

---

### POST /auth/api-keys
Create Api Key

Create a new API key for webhook authentication.

Requires owner or admin role.
Uses sub-account context so agency users create keys for the sub-account they're operating as.
The plaintext key is only returned ONCE - store it securely!

**Request Body:** `APIKeyCreate` (application/json)
- name: string
- expires_in_days: integer | null

**Responses:**
- `200`: Successful Response
  Returns: `APIKeyCreateResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /auth/api-keys/{key_id}
Delete Api Key

Delete an API key. Requires owner or admin role.

**Parameters:**
- `key_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/api-keys/{key_id}/revoke
Revoke Api Key

Revoke (deactivate) an API key without deleting it. Requires owner or admin role.

**Parameters:**
- `key_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /auth/context
Get Auth Context

Return tenant context for frontend navigation.

Returns:
- tenant_type: 'agency' | 'sub_account' | 'direct'
- current_tenant_id: UUID
- parent_tenant_id: UUID | None (for sub-accounts)
- available_sub_accounts: list (for agencies only)

**Responses:**
- `200`: Successful Response

---

### POST /auth/embed-sso
Embed Sso

Embedded SSO — authenticate via partner platform iframe integration.

Accepts an encrypted payload from the partner postMessage protocol,
decrypts it, maps the user to a Leadlock account, and returns
JWT tokens for the session.

Public endpoint - no auth required (SSO replaces login).

**Request Body:** `EmbedSSORequest` (application/json)
- payload: string (required) — Encrypted SSO payload from partner platform

**Responses:**
- `200`: Successful Response
  Returns: `AuthResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/forgot-password
Forgot Password

Send password reset email using Resend.

Generates a secure token, stores hash in DB, sends email via Resend.
This bypasses Supabase's email system for instant delivery.

Public endpoint - no auth required.

**Request Body:** `ForgotPasswordRequest` (application/json)
- email: string (required)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/login
Login

Login with email and password.
Returns access token, refresh token, user, and tenant info.

**Request Body:** `LoginRequest` (application/json)
- email: string (required)
- password: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `AuthResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/logout
Logout

Logout user.
Client should discard tokens. Server-side invalidation handled by Supabase.

**Responses:**
- `200`: Successful Response

---

### GET /auth/me
Get Me

Get current authenticated user and tenant info.
Requires valid access token in Authorization header.

**Responses:**
- `200`: Successful Response
  Returns: `MeResponse`

---

### POST /auth/refresh
Refresh

Refresh access token using refresh token.

**Request Body:** `RefreshTokenRequest` (application/json)
- refresh_token: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `AuthResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/reset-password
Reset Password

Reset password using our custom token.

Verifies token from password_reset_tokens table, then updates
the user's password via Supabase admin API.

Public endpoint - no auth required.

**Request Body:** `ResetPasswordRequest` (application/json)
- token: string (required) — Password reset token from email link
- new_password: string (required) — New password (minimum 6 characters)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/signup
Signup

Create a new user account.

Creates:
- Supabase Auth user
- Tenant record (direct or agency)
- User record with 'owner' role

Returns tokens for immediate login.

**Request Body:** `SignupRequest` (application/json)
- email: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)
- company_name: string (required)
- account_type: string enum ['direct', 'agency']
- tos_accepted: boolean — User must accept Terms of Service and Privacy Policy

**Responses:**
- `200`: Successful Response
  Returns: `AuthResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /auth/signup-pending
Create Pending Signup

Create a pending signup record and redirect to Stripe checkout.

Payment-First flow: Account is NOT created until Stripe payment succeeds.
Password is encrypted (not hashed) so it can be used to create the
Supabase Auth user after payment.

Public endpoint - no auth required.
Rate limited by middleware: 5 requests per minute for /auth/* endpoints.

**Request Body:** `PendingSignupRequest` (application/json)
- email: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)
- company_name: string (required)
- plan: string enum ['payg', 'starter', 'agency', 'pro']
- billing_period: string enum ['monthly', 'annual']
- tos_accepted: boolean — User must accept Terms of Service and Privacy Policy
- affiliate_code: string | null
- utm_source: string | null
- utm_medium: string | null
- utm_campaign: string | null
- utm_content: string | null
- utm_term: string | null
- referrer_url: string | null

**Responses:**
- `200`: Successful Response
  Returns: `PendingSignupResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Billing

### GET /billing
Get Subscription Status

Get current subscription status and usage summary.

**Responses:**
- `200`: Successful Response
  Returns: `SubscriptionStatus`

---

### POST /billing/apply-coupon
Apply Coupon

Apply a promotion code to an existing subscription.

Looks up the promotion code in Stripe, validates it's active,
and applies the associated coupon to the subscription.

**Request Body:** `ApplyCouponRequest` (application/json)
- promotion_code: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `ApplyCouponResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /billing/checkout
Create Checkout Session

Create a Stripe Checkout session for subscription signup.

Only tenant owner can initiate subscription.

**Request Body:** `CheckoutRequest` (application/json)
- plan: string enum ['payg', 'starter', 'agency', 'pro'] (required)
- billing_period: string enum ['monthly', 'annual']
- success_url: string | null
- cancel_url: string | null

**Responses:**
- `200`: Successful Response
  Returns: `CheckoutResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /billing/checkout-public
Create Public Checkout

Create Stripe checkout session for unauthenticated users (Stripe-first signup).

Account will be created via webhook after payment succeeds.
No authentication required - this is a public endpoint.

**Request Body:** `PublicCheckoutRequest` (application/json)
- email: string (required)
- plan: string enum ['payg', 'starter', 'agency', 'pro'] (required)
- billing_period: string enum ['monthly', 'annual']
- affiliate_code: string | null

**Responses:**
- `200`: Successful Response
  Returns: `CheckoutResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /billing/invoices
Get Invoices

Get invoice history from Stripe.

**Parameters:**
- `limit` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `InvoiceListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /billing/invoices/upcoming
Get Upcoming Invoice

Get upcoming invoice preview.

Shows what will be charged when trial ends or at next billing cycle.

**Responses:**
- `200`: Successful Response
  Returns: `UpcomingInvoiceResponse`

---

### GET /billing/limits
Get Tier Limits Endpoint

Get current tier limits and usage for the tenant.

Returns current counts vs limits for agents, sub-accounts, team members,
and share links, plus feature availability flags and voice rates.
Respects sub-account context when X-Sub-Account-Id header is present.

**Responses:**
- `200`: Successful Response
  Returns: `TierLimitsResponse`

---

### GET /billing/my-billing
Get My Billing

Get sub-account's billing info and usage for current period.

Sub-accounts don't have credit balances anymore (metered billing).
Shows usage this period and confirms billing goes to parent agency.

NOTE: Uses get_effective_tenant_id to support agency impersonation.
When agency user is "Operating as Sub-Account", the X-Sub-Account-Id
header is used to get the sub-account's billing info.

**Responses:**
- `200`: Successful Response
  Returns: `SubAccountBillingResponse`

---

### POST /billing/portal
Create Portal Session

Create a Stripe Customer Portal session with product filtering.

Shows only relevant upgrade options based on current tier:
- Starter: Agency/Pro upgrades
- Agency: Pro upgrade only
- Pro: White-Label addon

Allows customer to manage subscription, payment methods, and view invoices.
Only tenant owner can access portal.

**Request Body:** `PortalRequest` (application/json)
- return_url: string | null

**Responses:**
- `200`: Successful Response
  Returns: `PortalResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /billing/usage
Get Usage Records

Get usage records for the current billing period.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `UsageListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Calls

### GET /calls
List Calls

List call logs for the tenant.

Returns paginated call history with optional agent and direction filtering.
Respects sub-account context when X-Sub-Account-Id header is present.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `agent_id` (query, string | null) — Filter by agent
- `direction` (query, string | null) — Filter by direction (inbound, outbound, test, demo)

**Responses:**
- `200`: Successful Response
  Returns: `CallLogListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /calls/export
Export Calls

Export call logs as CSV.

**Parameters:**
- `agent_id` (query, string | null) — Filter by agent
- `status` (query, string | null) — Filter by status
- `date_from` (query, string | null) — Filter by start date
- `date_to` (query, string | null) — Filter by end date
- `search` (query, string | null) — Search term

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /calls/{call_id}
Get Call

Get details of a specific call.
Respects sub-account context when X-Sub-Account-Id header is present.

**Parameters:**
- `call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `CallLogResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /calls/{call_id}/analyze
Analyze Call

Analyze a call transcript using AI.

Returns insights about call outcome, summary, key moments, and actionable improvements.
Uses xAI to analyze the transcript and provide coaching feedback.

Respects sub-account context when X-Sub-Account-Id header is present.

**Parameters:**
- `call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /calls/{call_id}/recording
Get Call Recording

Stream recording audio for a specific call.

Proxies the audio from Twilio's authenticated API so the browser
can play it without needing Twilio credentials.
Respects sub-account context when X-Sub-Account-Id header is present.

Returns:
    StreamingResponse with audio/mpeg content

Raises:
    404: Call not found or no recording available

**Parameters:**
- `call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Chat

### GET /chat/conversations
List Conversations

List text conversations with pagination and filters.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `channel` (query, string | null)
- `text_assistant_id` (query, string | null)
- `date_from` (query, string | null)
- `date_to` (query, string | null)
- `search` (query, string | null)

**Responses:**
- `200`: Successful Response
  Returns: `TextConversationListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /chat/conversations/{conversation_id}
Get Conversation

Get a single conversation with assistant info.

**Parameters:**
- `conversation_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `TextConversationResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /chat/conversations/{conversation_id}/messages
List Messages

List messages for a conversation, ordered oldest-first.

**Parameters:**
- `conversation_id` (path, string (required))
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `TextMessageListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /chat/stats
Get Chat Stats

Get chat dashboard statistics.

**Parameters:**
- `date_from` (query, string | null)
- `date_to` (query, string | null)

**Responses:**
- `200`: Successful Response
  Returns: `ChatStatsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Compliance

### GET /compliance/outbound
Get Outbound Compliance

Get outbound calling compliance status for current tenant.

**Responses:**
- `200`: Successful Response
  Returns: `OutboundComplianceStatus`

---

### POST /compliance/outbound/accept
Accept Outbound Compliance

Accept outbound calling terms. Records acceptance with audit trail.

**Request Body:** `AcceptOutboundTermsRequest` (application/json)
- terms_version: string

**Responses:**
- `200`: Successful Response
  Returns: `OutboundComplianceStatus`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Contacts

### GET /contacts/
List Contacts

List GHL contacts with call statistics.

Returns paginated list of contacts enriched with:
- Total call count
- Last call date

Uses cursor-based pagination (GHL requirement). Pass BOTH `start_after_id` and
`start_after` from the previous response to get the next page.

For tenants with multiple GHL accounts, use integration_id to specify which one.
Use has_calls_only=true to filter to only contacts that have AI calls.

**Parameters:**
- `limit` (query, integer)
- `search` (query, string | null)
- `integration_id` (query, string | null) — Specific GHL integration ID for multi-account tenants
- `has_calls_only` (query, boolean) — Only show contacts with AI calls
- `enrich` (query, boolean) — Enrich with call stats (set false for fast search)
- `start_after_id` (query, string | null) — Cursor for pagination - contact ID from previous page's next_cursor
- `start_after` (query, integer | null) — Cursor timestamp from previous page's next_cursor_timestamp

**Responses:**
- `200`: Successful Response
  Returns: `ContactListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /contacts/with-calls
List Contacts With Calls

List only contacts that have AI call history.

Uses inverted data flow: queries call_logs first, then fetches GHL data.
This ensures ALL contacts with calls are found, not limited by GHL pagination.

Supports server-side sorting and filtering:
- sort_by: name, phone, email, company, calls, last_call
- sort_dir: asc, desc
- filter_phone/email/company: blank, not_blank

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `integration_id` (query, string | null) — Specific GHL integration ID for multi-account tenants
- `sort_by` (query, string | null) — Sort by: name, phone, email, company, calls, last_call
- `sort_dir` (query, string | null) — Sort direction: asc or desc
- `filter_phone` (query, string | null) — Filter phone: blank or not_blank
- `filter_email` (query, string | null) — Filter email: blank or not_blank
- `filter_company` (query, string | null) — Filter company: blank or not_blank

**Responses:**
- `200`: Successful Response
  Returns: `ContactListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /contacts/{phone}
Get Contact Detail

Get contact details with full call history.

Args:
    phone: Phone number (URL-encoded if contains special chars)
    enrich: Set to "full" for pipeline, custom fields, and appointment enrichment

**Parameters:**
- `phone` (path, string (required))
- `enrich` (query, string | null) — Set to 'full' for enriched contact data

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /contacts/{phone}
Patch Contact

Update a GHL contact: add/remove tags, update custom fields, update pipeline stage.

Each field is independently optional — partial success is OK.

**Parameters:**
- `phone` (path, string (required))

**Request Body:** `ContactPatchRequest` (application/json)
- add_tags: array of string
- remove_tags: array of string
- custom_fields: array of object | null
- opportunity_id: string | null
- pipeline_stage_id: string | null

**Responses:**
- `200`: Successful Response
  Returns: `ContactPatchResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /contacts/{phone}/conversations
Get Conversation Timeline

Get merged call + SMS conversation timeline for a contact.

Returns chronological list merging call_logs and text_messages.
Gracefully degrades to voice-only if GHL lookup fails (sms_included=false).
Never returns 404 — empty timeline is valid.

**Parameters:**
- `phone` (path, string (required))
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `ConversationTimelineResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /contacts/{phone}/notes
List Notes

List notes for a GHL contact.

**Parameters:**
- `phone` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `NotesListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /contacts/{phone}/notes
Create Note

Create a note on a GHL contact.

**Parameters:**
- `phone` (path, string (required))

**Request Body:** `NoteCreateRequest` (application/json)
- body: string (required)

**Responses:**
- `201`: Successful Response
  Returns: `NoteResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## D

### GET /d/showcase/{slug}
Get Showcase

Public endpoint: Get all active demos for a showcase page.
The slug here is any demo slug — we find the agent and return all demos for it.

**Parameters:**
- `slug` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /d/{slug}
Get Public Demo

Public endpoint: Get demo config for the demo page. No auth required.

**Parameters:**
- `slug` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `PublicDemoResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /d/{slug}/chat
Public Demo Chat

Public text chat endpoint for demo pages.
Uses the agent's system prompt + tools to generate AI text responses.
No auth required — authenticates via active demo config slug.

**Parameters:**
- `slug` (path, string (required))

**Request Body:** `DemoChatRequest` (application/json)
- messages: array of DemoChatMessage (required)
- dynamic_variables: object | null

**Responses:**
- `200`: Successful Response
  Returns: `DemoChatResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /d/{slug}/event
Track Demo Event

Public endpoint: Track a demo event (view, call, form submit).

**Parameters:**
- `slug` (path, string (required))

**Request Body:** `DemoEventCreate` (application/json)
- event_type: string (required)
- duration_s: integer | null
- metadata: object

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Demos

### GET /demos/
List Demos

List all demo configs for the current tenant.

**Responses:**
- `200`: Successful Response

---

### POST /demos/
Create Demo

Create a new demo config.

**Request Body:** `DemoConfigCreate` (application/json)
- agent_id: string (required)
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] (required)
- name: string (required)
- config: object
- after_cta_text: string | null
- after_cta_url: string | null
- webhook_url: string | null
- expires_in_days: integer | null

**Responses:**
- `200`: Successful Response
  Returns: `DemoConfigResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /demos/import-from-url
Import From Url

Import demo configuration from a website URL (non-streaming fallback).

Scrapes the provided URL, extracts business information using AI,
and generates personalized demo text (headline, summary, CTA).

Returns all fields needed to pre-fill the demo creation wizard.

Note: Prefer /import-from-url/stream for real-time progress updates.

**Request Body:** `ImportFromUrlRequest` (application/json)
- url: string (required) — Website URL to analyze (e.g., https://example.com)
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] (required) — Demo channel type

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /demos/import-from-url/stream
Import From Url Stream

Import demo configuration from a website URL with streaming progress updates.

Uses Server-Sent Events (SSE) to stream progress in real-time:
- Step updates: "discovering", "scraping", "extracting", "generating"
- Progress: current/total for each step
- Detail: what's currently being processed

Final event contains the complete ImportFromUrlResponse.

**Parameters:**
- `url` (query, string (required))
- `channel` (query, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /demos/templates
Get Templates

Get all industry demo templates.

**Responses:**
- `200`: Successful Response

---

### GET /demos/templates/{industry}/{channel}
Get Template

Get a specific industry/channel demo template.

**Parameters:**
- `industry` (path, string (required))
- `channel` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /demos/webhook-test
Test Webhook Url

Test any webhook URL by sending a sample payload. No demo ID needed.

**Request Body:** `WebhookUrlTestRequest` (application/json)
- webhook_url: string (required)
- form_fields: array of object | null

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /demos/{demo_id}
Get Demo

Get a single demo config.

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `DemoConfigResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /demos/{demo_id}
Update Demo

Update a demo config.

**Parameters:**
- `demo_id` (path, string (required))

**Request Body:** `DemoConfigUpdate` (application/json)
- name: string | null
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] | null
- config: object | null
- is_active: boolean | null
- after_cta_text: string | null
- after_cta_url: string | null
- webhook_url: string | null
- expires_in_days: integer | null

**Responses:**
- `200`: Successful Response
  Returns: `DemoConfigResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /demos/{demo_id}
Delete Demo

Delete a demo config.

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /demos/{demo_id}/analytics
Get Demo Analytics

Get analytics for a demo config.

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /demos/{demo_id}/duplicate
Duplicate Demo

Clone a demo config.

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `DemoConfigResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /demos/{demo_id}/upload-image
Upload Demo Image

Upload an image for a demo config (ad creative, logo, avatar, etc.).

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /demos/{demo_id}/webhook-test
Test Demo Webhook

Send a test payload to the demo's webhook URL.

**Parameters:**
- `demo_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Documents

### GET /documents
List Documents

List all documents for the current tenant.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: returns their documents.

**Responses:**
- `200`: Successful Response
  Returns: `DocumentListResponse`

---

### POST /documents
Upload Document

Upload a document to the knowledge base.

Supports 100+ file types (validated by xAI). Max 48MB.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: uploads to their collection.

**Responses:**
- `201`: Successful Response
  Returns: `DocumentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /documents/search
Search Documents

Search documents in the knowledge base.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: searches their collection.

**Request Body:** `SearchRequest` (application/json)
- query: string (required)
- max_results: integer

**Responses:**
- `200`: Successful Response
  Returns: `SearchResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /documents/stats
Get Stats

Get collection statistics for the current tenant.

Returns document counts, total size, and status breakdown.

**Responses:**
- `200`: Successful Response
  Returns: `CollectionStatsResponse`

---

### DELETE /documents/{document_id}
Delete Document

Delete a document from the knowledge base.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: deletes from their collection.

**Parameters:**
- `document_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Functions

### GET /functions
List Library Functions

List all custom functions in the tenant's library.

Returns functions with their attached agent information.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Responses:**
- `200`: Successful Response
  Returns: `FunctionLibraryResponse`

---

### POST /functions
Create Library Function

Create a new function in the tenant's library.

The function is not attached to any agent - use attach to add to agents.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Request Body:** `CustomFunctionCreate` (application/json)
- name: string (required) — Function name in snake_case (e.g., check_inventory)
- description: string (required) — Description of what the function does (shown to AI)
- parameters: object — JSON Schema for function parameters
- webhook_url: string (required) — Webhook URL to call (must start with http:// or https://)
- webhook_method: string — HTTP method for webhook call
- webhook_headers: object — Custom headers to include in webhook request
- webhook_timeout_ms: integer — Timeout for webhook call in milliseconds (1000-30000)
- is_enabled: boolean — Whether the function is enabled
- speak_during_execution: boolean — Whether AI should speak while waiting for webhook response

**Responses:**
- `201`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /functions/test-webhook
Test Webhook Url

Test a webhook URL before creating a function.

Makes a real HTTP request to the provided webhook URL to verify
connectivity and response. Used by the function wizard to validate
webhook URLs before saving.

**Request Body:** `WebhookTestRequest` (application/json)
- webhook_url: string (required) — Webhook URL to test
- webhook_method: string — HTTP method for webhook call
- webhook_headers: object — Custom headers to include in webhook request
- webhook_timeout_ms: integer — Timeout for webhook call in milliseconds
- function_name: string | null — Function name to include in test payload
- fields: array of WebhookTestField | null — Configured fields to build sample arguments from
- contact: WebhookTestContact | null — GHL contact to populate call_context with real data

**Responses:**
- `200`: Successful Response
  Returns: `FunctionTestResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /functions/{function_id}
Get Library Function

Get a specific function from the library with attached agents info.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `function_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `FunctionWithAgentsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PUT /functions/{function_id}
Update Library Function

Update a function in the library.

Changes affect all agents using this function.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `function_id` (path, string (required))

**Request Body:** `CustomFunctionUpdate` (application/json)
- name: string | null — Function name in snake_case
- description: string | null — Description of what the function does
- parameters: object | null — JSON Schema for function parameters
- webhook_url: string | null — Webhook URL to call
- webhook_method: string | null — HTTP method for webhook call
- webhook_headers: object | null — Custom headers to include in webhook request
- webhook_timeout_ms: integer | null — Timeout for webhook call in milliseconds
- is_enabled: boolean | null — Whether the function is enabled
- speak_during_execution: boolean | null — Whether AI should speak while waiting for webhook response

**Responses:**
- `200`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /functions/{function_id}
Delete Library Function

Delete a function from the library.

Cascade removes from all agents.
For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `function_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /functions/{function_id}/agents
List Function Agents

List all agents using a specific function.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `function_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /functions/{function_id}/copy
Copy Function To Sub Account

Copy a function to another sub-account (agency feature).

Requires agency access - the target tenant must be a sub-account
of the current agency.

**Parameters:**
- `function_id` (path, string (required))

**Request Body:** `CopyFunctionRequest` (application/json)
- target_tenant_id: string (required) — Target sub-account to copy function to

**Responses:**
- `200`: Successful Response
  Returns: `CustomFunctionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /functions/{function_id}/test
Test Library Function

Test a library function's webhook by making a real call.

For agencies: requires sub-account context (X-Sub-Account-Id header).

**Parameters:**
- `function_id` (path, string (required))

**Request Body:** `FunctionTestRequest` (application/json)
- arguments: object — Arguments to pass to the function
- contact_id: string — GHL contact ID — always present via Contact Intelligence

**Responses:**
- `200`: Successful Response
  Returns: `FunctionTestResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Health

### GET /health
Health Check

Health check endpoint. Returns 503 during graceful shutdown drain.

**Responses:**
- `200`: Successful Response

---

## Integrations

### GET /integrations
List Integrations

List all connected integrations for the current tenant.
Supports sub-account context via X-Sub-Account-Id header.

For sub-accounts: Returns integrations ASSIGNED via sub_account_integrations table.
For regular tenants: Returns integrations directly owned by the tenant.

**Responses:**
- `200`: Successful Response

---

### GET /integrations/calendar/auth
Ghl Auth Initiate

Initiate GHL OAuth flow.

Returns the OAuth URL for the user to authorize access.

Supports agency impersonation: If X-Sub-Account-Id header is present,
the integration will be created for the sub-account's tenant.

**Responses:**
- `200`: Successful Response

---

### GET /integrations/calendar/callback
Ghl Auth Callback

Handle GHL OAuth callback.

Exchanges the authorization code for tokens and stores them.
Supports two flows:
- User-initiated (from our app): state parameter present with tenant_id
- Marketplace install (from GHL): no state parameter, tenant resolved from token response

**Parameters:**
- `code` (query, string (required))
- `state` (query, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/calendars
List Ghl Calendars

List available GoHighLevel calendars for a specific integration.

Args:
    integration_id: The UUID of the GHL integration to fetch calendars from.
                   Use GET /integrations/ghl/integrations to list available integrations.
Supports sub-account context via X-Sub-Account-Id header.

**Parameters:**
- `integration_id` (query, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /integrations/ghl/connect-api-key
Connect Ghl Api Key

Connect GoHighLevel using a Private Integration API key.

Alternative to OAuth for when marketplace approval is pending.
Validates the key against GHL API, encrypts, and stores.

Args:
    request: API key and location ID
    current_user: Current authenticated user
    tenant_id: Current tenant ID (supports sub-account context)

Returns:
    Success status with location name

Raises:
    HTTPException 400: If API key is invalid or location not found

**Request Body:** `GHLApiKeyRequest` (application/json)
- api_key: string (required) — GHL Private Integration API key
- location_id: string (required) — GHL Location ID

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /integrations/ghl/disconnect
Disconnect Ghl

DEPRECATED: Disconnect GoHighLevel integration.

This endpoint deactivates ALL GHL integrations for the tenant.
Use DELETE /integration/{integration_id} instead to disconnect a specific integration.

Removes stored OAuth tokens and deactivates integration.

NOTE: Uses the user's ACTUAL tenant_id (not sub-account context) because
integrations are always owned by the tenant that connected them.

**Responses:**
- `200`: Successful Response

---

### GET /integrations/ghl/integrations
List Ghl Integrations

List all GoHighLevel integrations available to the tenant.
Includes both:
- Integrations owned directly by this tenant
- Integrations assigned to this sub-account from parent agency
Supports sub-account context via X-Sub-Account-Id header.

**Responses:**
- `200`: Successful Response

---

### GET /integrations/ghl/phone-numbers
List Ghl Phone Numbers

List phone numbers from GoHighLevel location.

NOTE: GHL API does not support adding phone numbers programmatically.
This is display-only - users must manually import numbers via GHL UI.

Args:
    integration_id: Optional specific GHL integration ID to fetch numbers from.
                   If not provided, uses first active GHL integration.

Returns:
    List of phone numbers formatted for frontend:
    - phone_number: E.164 format
    - friendly_name: Display name
    - capabilities: {voice: bool, sms: bool, mms: bool}
Supports sub-account context via X-Sub-Account-Id header.

**Parameters:**
- `integration_id` (query, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/status
Get Ghl Status

Get GoHighLevel integration connection status.

Returns connection status and location information.
Supports sub-account context via X-Sub-Account-Id header.

Checks both:
- Integrations owned directly by this tenant
- Integrations assigned to this sub-account from parent agency

**Responses:**
- `200`: Successful Response

---

### GET /integrations/ghl/timezones
List Ghl Timezones

Return the IANA timezones GHL supports for the current tenant's sub-account.

Picks any active GHL integration on the tenant (or assigned to this sub-account)
and calls GET /locations/:locationId/timezones. Result is cached in-process for
7 days since GHL's list is effectively static.

Returns an empty list if no active GHL integration exists — frontend falls back
to the full IANA set via Intl.supportedValuesOf('timeZone').

**Responses:**
- `200`: Successful Response

---

### GET /integrations/ghl/{integration_id}/custom-fields
List Ghl Custom Fields

List available custom fields from GoHighLevel location.

Returns all custom fields configured in the GHL location that can be
updated via the update_custom_fields tool.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/{integration_id}/location-details
Get Ghl Location Details

Fetch full location details from GoHighLevel API.

Returns location name, email, phone, address, and other details
to auto-fill sub-account creation form.

Supports both direct ownership and junction table assignment for sub-accounts.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/{integration_id}/pipelines
List Ghl Pipelines

List available pipelines from GoHighLevel location.

Returns all pipelines and their stages configured in the GHL location
that can be used with create_opportunity/update_opportunity_stage tools.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/{integration_id}/tags
List Ghl Tags

List available tags from GoHighLevel location.

Returns all tags configured in the GHL location that can be
applied to contacts via the add_tag/remove_tag tools.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /integrations/ghl/{integration_id}/tags
Create Ghl Tag

Create a new tag in the GoHighLevel location.

Body: { "name": "tag-name" }

**Parameters:**
- `integration_id` (path, string (required))

**Request Body:** object (application/json)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /integrations/ghl/{integration_id}/workflows
List Ghl Workflows

List available workflows from GoHighLevel location.

Returns all workflows configured in the GHL location that can be
triggered via the trigger_workflow tool.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /integrations/integration/{integration_id}
Disconnect Integration By Id

Disconnect a specific integration by ID.

This removes the stored tokens but doesn't revoke access at the provider.
Allows disconnecting individual integrations when multiple of the same provider exist.

NOTE: Uses the user's ACTUAL tenant_id (not sub-account context) because
integrations are always owned by the tenant that connected them, not sub-accounts.
Sub-accounts only have integration ASSIGNMENTS via sub_account_integrations table.

**Parameters:**
- `integration_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /integrations/twilio/connect
Connect Twilio

Connect tenant's Twilio account with API credentials.

Unlike OAuth integrations, this accepts credentials directly.
Credentials are validated by testing API connection before saving.

Args:
    request: Account SID and Auth Token
    current_user: Current authenticated user
    tenant_id: Current tenant ID

Returns:
    Success status and saved integration data

Raises:
    HTTPException 400: If credentials are invalid

**Request Body:** `TwilioCredentialsRequest` (application/json)
- account_name: string (required) — Friendly name for this Twilio account
- account_sid: string (required) — Twilio Account SID (ACxxxxxx...)
- auth_token: string (required) — Twilio Auth Token

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /integrations/twilio/disconnect
Disconnect Twilio

Disconnect tenant's Twilio account.

Removes stored credentials from database.
Phone numbers provisioned with this account will stop working.

Args:
    current_user: Current authenticated user
    tenant_id: Current tenant ID

Returns:
    Success status

Raises:
    HTTPException 404: If no Twilio integration found

**Responses:**
- `200`: Successful Response

---

### GET /integrations/twilio/status
Get Twilio Status

Check Twilio integration status with live credential validation.

Makes a real Twilio API call to verify credentials are valid and the
account is in good standing (not suspended, negative balance, etc.).

Args:
    current_user: Current authenticated user
    tenant_id: Current tenant ID

Returns:
    Connection status, health status, masked account SID, metadata

**Responses:**
- `200`: Successful Response

---

### DELETE /integrations/{provider}
Disconnect Integration

DEPRECATED: Disconnect an integration by provider name.

This endpoint deletes ALL integrations of the given provider type.
Use DELETE /integration/{integration_id} instead to delete a specific integration.

This removes the stored tokens but doesn't revoke access at the provider.

NOTE: Uses the user's ACTUAL tenant_id (not sub-account context) because
integrations are always owned by the tenant that connected them.

**Parameters:**
- `provider` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Issues

### POST /issues/
Create Issue

Submit an issue report with optional screenshot.

**Responses:**
- `201`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Knowledge Bases

### GET /knowledge-bases
List Knowledge Bases

List all Knowledge Bases for the current tenant.

For agencies: requires sub-account context (X-Sub-Account-Id header).
For direct tenants: returns their Knowledge Bases.

**Responses:**
- `200`: Successful Response
  Returns: `KnowledgeBaseListResponse`

---

### POST /knowledge-bases
Create Knowledge Base

Create a new Knowledge Base.

Creates an xAI collection for document storage.

**Request Body:** `KnowledgeBaseCreate` (application/json)
- name: string (required) — Name of the Knowledge Base

**Responses:**
- `201`: Successful Response
  Returns: `KnowledgeBaseResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}
Get Knowledge Base

Get a specific Knowledge Base by ID.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `KnowledgeBaseResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /knowledge-bases/{kb_id}
Update Knowledge Base

Update a Knowledge Base (rename).

**Parameters:**
- `kb_id` (path, string (required))

**Request Body:** `KnowledgeBaseUpdate` (application/json)
- name: string (required) — New name for the Knowledge Base

**Responses:**
- `200`: Successful Response
  Returns: `KnowledgeBaseResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /knowledge-bases/{kb_id}
Delete Knowledge Base

Delete a Knowledge Base and all its documents.

This also removes the KB from any agents that reference it.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/documents
List Kb Documents

List all documents in a specific Knowledge Base.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `DocumentListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/documents
Upload Kb Document

Upload a document to a specific Knowledge Base.

Supports 100+ file types (validated by xAI). Max 48MB.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `201`: Successful Response
  Returns: `DocumentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/faqs
List Faq Sources

List all FAQ sources for a KB with their pairs.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/faqs
Create Faq Source

Create an FAQ source with optional initial pairs.

**Parameters:**
- `kb_id` (path, string (required))

**Request Body:** `FAQSourceCreate` (application/json)
- name: string (required)
- pairs: array of FAQPairCreate

**Responses:**
- `201`: Successful Response
  Returns: `FAQSourceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/faqs/{source_id}
Get Faq Source

Get an FAQ source with all its pairs.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `FAQSourceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/faqs/{source_id}/generate
Generate Faqs

Use AI to generate FAQ pairs from provided content.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Request Body:** `GenerateFAQRequest` (application/json)
- content: string (required) — Content to extract FAQs from
- num_pairs: integer

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/faqs/{source_id}/pairs
Add Faq Pairs

Add FAQ pairs to an existing FAQ source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Request Body:** array of FAQPairCreate (application/json)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /knowledge-bases/{kb_id}/faqs/{source_id}/pairs/{pair_id}
Update Faq Pair

Update a single FAQ pair.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))
- `pair_id` (path, string (required))

**Request Body:** `FAQPairUpdate` (application/json)
- question: string | null
- answer: string | null
- sort_order: integer | null

**Responses:**
- `200`: Successful Response
  Returns: `FAQPairResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /knowledge-bases/{kb_id}/faqs/{source_id}/pairs/{pair_id}
Delete Faq Pair

Delete a single FAQ pair.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))
- `pair_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/rich-text
List Rich Texts

List all rich text sources for a KB.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/rich-text
Create Rich Text

Create a rich text source and sync to xAI.

**Parameters:**
- `kb_id` (path, string (required))

**Request Body:** `RichTextCreate` (application/json)
- name: string (required)
- content: string (required) — Rich text / markdown content

**Responses:**
- `201`: Successful Response
  Returns: `RichTextResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/rich-text/{source_id}
Get Rich Text

Get a rich text source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `RichTextResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /knowledge-bases/{kb_id}/rich-text/{source_id}
Update Rich Text

Update a rich text source and re-sync to xAI.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Request Body:** `RichTextUpdate` (application/json)
- name: string | null
- content: string | null

**Responses:**
- `200`: Successful Response
  Returns: `RichTextResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/sources
List Sources

List all sources for a Knowledge Base, optionally filtered by type.

**Parameters:**
- `kb_id` (path, string (required))
- `source_type` (query, string | null)

**Responses:**
- `200`: Successful Response
  Returns: `SourceListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /knowledge-bases/{kb_id}/sources/{source_id}
Delete Source

Delete a KB source and its linked xAI document.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/stats
Get Kb Stats

Get statistics for a specific Knowledge Base.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `CollectionStatsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/tables
List Tables

List all table sources for a KB.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/tables
Create Table Source

Create a table source and sync to xAI.

**Parameters:**
- `kb_id` (path, string (required))

**Request Body:** `TableSourceCreate` (application/json)
- name: string (required)
- headers: array of string (required)
- table_data: array of array of string

**Responses:**
- `201`: Successful Response
  Returns: `TableSourceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/tables/parse-csv
Parse Csv

Parse a CSV file and return headers + rows (does not create a source).

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/tables/{source_id}
Get Table Source

Get a table source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `TableSourceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /knowledge-bases/{kb_id}/tables/{source_id}
Update Table Source

Update a table source and re-sync to xAI.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Request Body:** `TableSourceUpdate` (application/json)
- name: string | null
- headers: array of string | null
- table_data: array of array of string | null

**Responses:**
- `200`: Successful Response
  Returns: `TableSourceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/web-crawlers
List Web Crawlers

List all web crawler sources for a KB.

**Parameters:**
- `kb_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/web-crawlers
Create Web Crawler

Create a web crawler source and trigger initial crawl.

**Parameters:**
- `kb_id` (path, string (required))

**Request Body:** `WebCrawlerCreate` (application/json)
- name: string (required)
- root_url: string (required) — URL to crawl
- schedule_interval: string | null — Recrawl interval: 'daily', 'weekly', 'monthly', or None

**Responses:**
- `201`: Successful Response
  Returns: `WebCrawlerResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /knowledge-bases/{kb_id}/web-crawlers/{source_id}
Get Web Crawler

Get a web crawler source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `WebCrawlerResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /knowledge-bases/{kb_id}/web-crawlers/{source_id}/recrawl
Trigger Recrawl

Trigger a re-crawl of the web source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `WebCrawlerResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /knowledge-bases/{kb_id}/web-crawlers/{source_id}/schedule
Update Crawl Schedule

Update the recrawl schedule for a web crawler source.

**Parameters:**
- `kb_id` (path, string (required))
- `source_id` (path, string (required))

**Request Body:** `WebCrawlerScheduleUpdate` (application/json)
- schedule_interval: string | null — Recrawl interval: 'daily', 'weekly', 'monthly', or None

**Responses:**
- `200`: Successful Response
  Returns: `WebCrawlerResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Notifications

### GET /notifications/in-app
List In App Notifications

List in-app notifications for the current tenant (or sub-account context).

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `NotificationListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /notifications/in-app/aggregate
List Aggregate Notifications

List notifications across all sub-accounts (agency owners only).

Uses get_current_tenant_id (not effective) so we always query from
the agency owner's perspective, even when in sub-account context.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)

**Responses:**
- `200`: Successful Response
  Returns: `NotificationListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /notifications/in-app/aggregate/unread-count
Get Aggregate Unread Count

Get aggregate unread count across all sub-accounts.

**Responses:**
- `200`: Successful Response
  Returns: `UnreadCountResponse`

---

### DELETE /notifications/in-app/clear
Clear Read Notifications

Delete all read notifications for the tenant. Keeps unread ones.

**Responses:**
- `200`: Successful Response

---

### PATCH /notifications/in-app/read-all
Mark All Notifications Read

Mark all notifications as read.

**Responses:**
- `200`: Successful Response

---

### GET /notifications/in-app/unread-count
Get Unread Count

Get unread notification count for badge polling.

**Responses:**
- `200`: Successful Response
  Returns: `UnreadCountResponse`

---

### DELETE /notifications/in-app/{notification_id}
Delete Notification

Delete a single notification.

**Parameters:**
- `notification_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /notifications/in-app/{notification_id}/read
Mark Notification Read

Mark a single notification as read.

**Parameters:**
- `notification_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /notifications/settings
Get Notification Settings

Get notification settings for the current tenant.

Returns default settings if none exist (creating them in the process).

**Responses:**
- `200`: Successful Response
  Returns: `NotificationSettingsResponse`

---

### PATCH /notifications/settings
Update Notification Settings

Update notification settings for the current tenant.

Only provided fields are updated; others remain unchanged.

**Request Body:** `NotificationSettingsUpdate` (application/json)
- email_new_call: boolean | null
- email_call_summary: boolean | null
- email_low_balance: boolean | null
- email_weekly_digest: boolean | null
- additional_emails: array of string | null
- quiet_hours_enabled: boolean | null
- quiet_hours_start: string | null
- quiet_hours_end: string | null
- quiet_hours_timezone: string | null
- notification_frequency: string enum ['immediate', 'daily', 'weekly'] | null
- sms_enabled: boolean | null

**Responses:**
- `200`: Successful Response
  Returns: `NotificationSettingsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Onboarding

### PUT /onboarding/navigate/{step}
Navigate To Step

Navigate to a specific step (back button / sidebar click).
Only allows navigating to completed steps or current step.

**Parameters:**
- `step` (path, integer (required))

**Responses:**
- `200`: Successful Response
  Returns: `OnboardingProgress`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /onboarding/progress
Get Onboarding Progress

Get current onboarding progress for the tenant.
Creates a new record if none exists.

**Responses:**
- `200`: Successful Response
  Returns: `OnboardingProgress`

---

### PUT /onboarding/progress/{step}
Update Onboarding Progress

Update onboarding progress for a specific step.
Marks the step as complete and advances to the next step.

**Parameters:**
- `step` (path, integer (required))

**Request Body:** `StepUpdateRequest` (application/json)
- account_type: string | null
- business_name: string | null
- industry: string | null
- connected: boolean | null
- purchased: boolean | null
- created: boolean | null
- completed: boolean | null
- deployed: boolean | null
- skipped: boolean | null
- agent_id: string | null
- ghl_integration_id: string | null
- phone_number_id: string | null
- sub_account_id: string | null

**Responses:**
- `200`: Successful Response
  Returns: `OnboardingProgress`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /onboarding/reset
Reset Onboarding Progress

Reset onboarding progress to step 1.
Useful for testing or allowing users to restart the wizard.

**Responses:**
- `200`: Successful Response
  Returns: `OnboardingProgress`

---

### POST /onboarding/skip/{step}
Skip Onboarding Step

Skip an optional onboarding step.
Only steps 2 (CRM), 3 (Phone), and 7 (Complete) can be skipped.

**Parameters:**
- `step` (path, integer (required))

**Responses:**
- `200`: Successful Response
  Returns: `OnboardingProgress`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Outbound

### POST /outbound/agents/{agent_id}/call
Initiate Outbound Call

Initiate an outbound call from a voice agent.

The agent will call the specified phone number and handle the conversation
using its configured AI settings.

Args:
    agent_id: The agent to handle the call
    request: Call details including recipient number

Returns:
    Call details including call_sid for tracking

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `OutboundCallRequest` (application/json)
- to_number: string (required) — Recipient phone number in E.164 format (e.g., +14155551234)
- from_phone_number_id: string | null — Specific phone number to call from. If not provided, uses agent's primary number.
- ghl_contact_id: string | null — GHL contact ID for pre-flight conversation checks

**Responses:**
- `200`: Successful Response
  Returns: `OutboundCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /outbound/trigger
Trigger Outbound Call

Trigger an outbound call via webhook (for GHL, Zapier, etc.).

Authentication: API Key (X-API-Key header) or JWT Bearer token.

This endpoint is designed for external automation triggers like:
- GoHighLevel workflow webhooks
- Zapier/Make integrations
- Custom automation scripts

Args:
    request: Webhook payload with agent_id, to_number, and optional context

Returns:
    Call details including call_sid for tracking

Example cURL:
```
curl -X POST https://leadlock-app.onrender.com/outbound/trigger \
  -H "X-API-Key: sk_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "uuid-here",
    "to_number": "+14155551234",
    "context": {
      "first_name": "John",
      "source": "GHL New Lead"
    }
  }'
```

**Request Body:** `WebhookTriggerRequest` (application/json)
- agent_id: string (required) — Agent ID to handle the call
- to_number: string (required) — Recipient phone number in E.164 format
- from_phone_number_id: string | null — Specific phone number to call from
- ghl_contact_id: string | null — GHL contact ID for pre-flight conversation checks
- context: WebhookCallContext | null — Context to personalize the call (injected into agent prompt)
- dynamic_variables: object | null — Variables to substitute in prompt: {'customer_name': 'John', 'order_id': '12345'}. All values must be strings.

**Responses:**
- `200`: Successful Response
  Returns: `OutboundCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Phone Numbers

### GET /phone-numbers
List Phone Numbers

List all phone numbers owned by the tenant.
For sub-accounts (or agencies viewing as sub-account), only shows numbers assigned to them.

**Parameters:**
- `sub_account_id` (query, string | null) — Filter by sub-account

**Responses:**
- `200`: Successful Response
  Returns: `PhoneNumberListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers
Purchase Phone Number

Purchase a phone number.

The number will be registered with Twilio and configured with
the appropriate webhook URLs for voice calls.

NOTE: Only agencies can purchase phone numbers (not sub-accounts).
Agencies must be in agency view (not viewing as sub-account).

**Request Body:** `PhoneNumberPurchase` (application/json)
- phone_number: string (required) — E.164 format: +14155551234

**Responses:**
- `200`: Successful Response
  Returns: `PhoneNumberResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /phone-numbers/available-for-assignment
Get Available For Assignment

Get all phone numbers available for assignment to sub-accounts.
Only returns agency's own numbers (not sub-account imported ones).

**Responses:**
- `200`: Successful Response

---

### POST /phone-numbers/backfill-sms-webhooks
Backfill Sms Webhooks

One-time backfill: set SMS webhook URL on all Twilio SMS-capable numbers
for the current tenant. Safe to call multiple times (idempotent).

**Responses:**
- `200`: Successful Response

---

### POST /phone-numbers/import
Import Phone Numbers

Import one or more phone numbers from Twilio account.

Imports numbers with automatic webhook configuration for voice calls.
Limited to 10 numbers per request to avoid rate limits and timeouts.

**Request Body:** `ImportNumbersRequest` (application/json)
- phone_number_sids: array of string (required) — List of Twilio phone number SIDs to import
- configure_sip: boolean — DEPRECATED - No longer used (kept for API compatibility)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers/import/ghl
Import Ghl Phone Numbers

Import one or more GoHighLevel phone numbers.

GHL numbers are imported as SMS-capable (no voice) for future
SMS/chat integration via Lead Connector.

Limited to 10 numbers per request.

**Request Body:** `ImportGHLNumbersRequest` (application/json)
- phone_numbers: array of object (required) — List of GHL phone numbers to import

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers/refresh-a2p-status
Refresh All A2P Status

Refresh A2P status for all phone numbers belonging to current tenant.

This endpoint:
- Checks A2P status for ALL tenant phone numbers
- Updates database with current status
- Returns summary of results

Use cases:
- After completing A2P registration in Twilio/GHL
- Periodic status verification
- Troubleshooting messaging issues

**Responses:**
- `200`: Successful Response

---

### GET /phone-numbers/search
Search Available Numbers

Search for available phone numbers to purchase.

Returns a list of available numbers matching the criteria.

**Parameters:**
- `area_code` (query, string | null) — Filter by area code
- `country` (query, string) — ISO country code
- `contains` (query, string | null) — Pattern to search for
- `limit` (query, integer) — Max results

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /phone-numbers/twilio/list
List Twilio Numbers

List all numbers in client's Twilio account.

Returns numbers with import status indicating whether each number
is already imported, available for import, or unavailable.

**Responses:**
- `200`: Successful Response

---

### GET /phone-numbers/{phone_number_id}
Get Phone Number

Get details of a specific phone number.

**Parameters:**
- `phone_number_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `PhoneNumberResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /phone-numbers/{phone_number_id}
Update Phone Number

Update a phone number's properties.

Use this to assign a phone number to an agent or update its friendly name.

**Parameters:**
- `phone_number_id` (path, string (required))

**Request Body:** `PhoneNumberUpdate` (application/json)
- agent_id: string | null — Assign to agent
- friendly_name: string | null — Display name

**Responses:**
- `200`: Successful Response
  Returns: `PhoneNumberResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /phone-numbers/{phone_number_id}
Release Phone Number

Delete a phone number from Leadlock.

IMPORTANT: This only removes the number from Leadlock's database.
The number remains in your Twilio/GoHighLevel account and can be re-imported.

To permanently release a number from Twilio (so it can be purchased by others),
use the Twilio Console.

**Parameters:**
- `phone_number_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers/{phone_number_id}/assign
Assign Phone Number

Assign a phone number to a sub-account.
Pass sub_account_id=null to unassign.
Only agencies can use this endpoint.

**Parameters:**
- `phone_number_id` (path, string (required))

**Request Body:** `AssignPhoneNumberRequest` (application/json)
- sub_account_id: string | null — Sub-account ID to assign to, or None to unassign

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers/{phone_number_id}/check-a2p
Check A2P Status

Check and update A2P registration status for a phone number.

This endpoint:
- Queries Twilio/GHL API to check A2P status
- Updates database with current status
- Returns A2P details and messaging_enabled flag

Use this after completing A2P registration to verify status.

**Parameters:**
- `phone_number_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /phone-numbers/{phone_number_id}/test-sms
Send Test Sms

Send a test SMS message using the specified phone number.

This endpoint:
- Validates phone number is SMS-capable
- Validates A2P registration (required for US numbers)
- Routes to Twilio or GoHighLevel based on phone number source
- Returns delivery status

Requirements:
- Phone number must be sms_capable = true
- Phone number must have messaging_enabled = true (A2P verified)
- Recipient number must be in E.164 format (+14155551234)

NOTE: Uses get_effective_tenant_id so sub-account users (or agency users
impersonating a sub-account) are correctly attributed in text metering
(FORGE text-agent-metering Step 9, 2026-04-08 — Site #10 / Issue #148 pattern).

Args:
    phone_number_id: UUID of phone number to send from
    to: Recipient phone number (E.164 format)
    message: Message text (optional, defaults to test message)

Returns:
    SMSResult with delivery status and provider details

**Parameters:**
- `phone_number_id` (path, string (required))
- `to` (query, string (required)) — Recipient phone number (E.164 format, e.g., +14155551234)
- `message` (query, string) — Message text

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## SMS Pools

### GET /sms-pools/
List Pools

List active pools for the current tenant (owned or sub-account).

**Responses:**
- `200`: Successful Response

---

### POST /sms-pools/import
Import Pool

Create a pool by importing an existing Twilio Messaging Service.

**Request Body:** `MSImportRequest` (application/json)
- messaging_service_sid: string (required)
- integration_id: string (required)
- name: string | null

**Responses:**
- `201`: Successful Response
  Returns: `PoolResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sms-pools/import/list-services
List Available Services

List Twilio Messaging Services across all the tenant's Twilio integrations.

**Responses:**
- `200`: Successful Response

---

### GET /sms-pools/{pool_id}
Get Pool

Fetch a single pool with members + today's per-member stats.

**Parameters:**
- `pool_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `PoolResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /sms-pools/{pool_id}
Delete Pool

Soft-delete the pool (Twilio MS remains untouched — customer owns it).

**Parameters:**
- `pool_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sms-pools/{pool_id}/sync
Sync Pool

Reconcile local members with current Twilio MS membership (non-destructive).

**Parameters:**
- `pool_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `PoolResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Scheduled Calls

### GET /scheduled-calls
List Scheduled Calls

List scheduled calls for the current tenant.

Supports filtering by status, agent, and date range.
Returns soonest calls first.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `status` (query, string | null) — Filter by status: pending, dialing, completed, failed, cancelled
- `agent_id` (query, string | null) — Filter by agent
- `start_date` (query, string | null) — Filter by scheduled_for >= start_date
- `end_date` (query, string | null) — Filter by scheduled_for <= end_date

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /scheduled-calls
Create Scheduled Call

Create a new scheduled call (manual scheduling from UI).

For AI-driven scheduling, use the schedule_callback function during a call.

**Request Body:** `ScheduledCallCreate` (application/json)
- agent_id: string (required)
- to_phone_number: string (required) — Recipient phone number in E.164 format
- scheduled_for: string (required) — When to call (ISO 8601 format, will be stored as UTC)
- timezone: string — User's timezone for display purposes
- contact_id: string | null — GHL contact ID if known
- contact_name: string | null — Contact name for display
- phone_number_id: string | null — Specific phone number to call from (uses agent default if not provided)
- is_callback: boolean — True if this is a return call
- previous_call_log_id: string | null — ID of the call that requested this callback
- callback_context: string | null — Summary of previous conversation for context-aware greeting

**Responses:**
- `201`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /scheduled-calls/{scheduled_call_id}
Get Scheduled Call

Get a specific scheduled call by ID.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /scheduled-calls/{scheduled_call_id}
Update Scheduled Call

Update a scheduled call.

Only pending calls can be updated.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Request Body:** `ScheduledCallUpdate` (application/json)
- scheduled_for: string | null
- timezone: string | null
- status: string enum ['pending', 'cancelled'] | null
- contact_name: string | null

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /scheduled-calls/{scheduled_call_id}
Delete Scheduled Call

Delete a scheduled call.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /scheduled-calls/{scheduled_call_id}/cancel
Cancel Scheduled Call

Cancel a pending scheduled call.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /scheduled-calls/{scheduled_call_id}/retry
Retry Scheduled Call

Retry a failed scheduled call.

If no new time is provided, schedules for 5 minutes from now.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Request Body:** `ScheduledCallRetry` (application/json)
- scheduled_for: string | null — New time to schedule. If not provided, schedules immediately.

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /scheduled-calls/{scheduled_call_id}/trigger
Trigger Scheduled Call

Immediately trigger a pending scheduled call.

Bypasses the scheduler wait and dials right away.

**Parameters:**
- `scheduled_call_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `ScheduledCallResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Sequences

### GET /sequences
List Sequences

List sequences for the current tenant.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `is_active` (query, boolean | null)

**Responses:**
- `200`: Successful Response
  Returns: `SequenceListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sequences
Create Sequence

Create a new sequence.

**Request Body:** `SequenceCreate` (application/json)
- name: string (required)
- description: string | null
- agent_id: string (required)
- phone_number_id: string | null
- pool_id: string | null
- active_tag: string | null
- continuous_add: boolean
- steps: array of SequenceStep (required)
- max_attempts: integer
- stop_on_booking: boolean
- stop_on_reply: boolean
- operating_hours: OperatingHours | null
- template_id: string | null
- qualification_criteria: string | null

**Responses:**
- `201`: Successful Response
  Returns: `SequenceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sequences/templates
Get Templates

List available sequence templates.

**Responses:**
- `200`: Successful Response

---

### POST /sequences/webhook/trigger
Webhook Enrollment Trigger

GHL workflow triggers enrollment via this webhook.

Accepts API key via Authorization header (preferred) or query param (legacy).
The Authorization header avoids key exposure in server/proxy access logs.

**Parameters:**
- `api_key` (query, string | null) — Tenant API key (prefer Authorization header)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sequences/{sequence_id}
Get Sequence

Get a sequence by ID.

**Parameters:**
- `sequence_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `SequenceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /sequences/{sequence_id}
Update Sequence

Update a sequence.

**Parameters:**
- `sequence_id` (path, string (required))

**Request Body:** `SequenceUpdate` (application/json)
- name: string | null
- description: string | null
- agent_id: string | null
- phone_number_id: string | null
- pool_id: string | null
- active_tag: string | null
- continuous_add: boolean | null
- steps: array of SequenceStep | null
- max_attempts: integer | null
- stop_on_booking: boolean | null
- stop_on_reply: boolean | null
- operating_hours: OperatingHours | null
- qualification_criteria: string | null

**Responses:**
- `200`: Successful Response
  Returns: `SequenceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /sequences/{sequence_id}
Delete Sequence

Delete a sequence. Must be inactive first.

**Parameters:**
- `sequence_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sequences/{sequence_id}/activate
Activate Sequence

Activate a sequence.

**Parameters:**
- `sequence_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `SequenceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sequences/{sequence_id}/deactivate
Deactivate Sequence

Deactivate a sequence.

**Parameters:**
- `sequence_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `SequenceResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sequences/{sequence_id}/enrollments
List Enrollments

List enrollments for a sequence.

**Parameters:**
- `sequence_id` (path, string (required))
- `limit` (query, integer)
- `offset` (query, integer)
- `status` (query, string | null)

**Responses:**
- `200`: Successful Response
  Returns: `EnrollmentListResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sequences/{sequence_id}/enrollments
Enroll Contact

Enroll a single contact into a sequence.

**Parameters:**
- `sequence_id` (path, string (required))

**Request Body:** `EnrollmentCreate` (application/json)
- contact_phone: string (required) — E.164 format
- contact_name: string | null
- contact_email: string | null
- contact_id: string | null
- timezone: string

**Responses:**
- `201`: Successful Response
  Returns: `EnrollmentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /sequences/{sequence_id}/enrollments/csv
Csv Import

Bulk enroll contacts from CSV data.

**Parameters:**
- `sequence_id` (path, string (required))

**Request Body:** `CSVImportRequest` (application/json)
- rows: array of object (required) — Parsed CSV rows with mapped field names
- field_mapping: object (required) — CSV column → schema field mapping

**Responses:**
- `200`: Successful Response
  Returns: `CSVImportResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /sequences/{sequence_id}/enrollments/{enrollment_id}
Cancel Enrollment

Cancel an enrollment.

**Parameters:**
- `sequence_id` (path, string (required))
- `enrollment_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sequences/{sequence_id}/enrollments/{enrollment_id}/dispositions
Get Enrollment Dispositions

Get disposition log for an enrollment.

**Parameters:**
- `sequence_id` (path, string (required))
- `enrollment_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /sequences/{sequence_id}/stats
Get Stats

Get enrollment stats for a sequence.

**Parameters:**
- `sequence_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `SequenceStats`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Setup

### GET /setup/status
Get Setup Status

Get setup completion status derived from real tenant data.

**Responses:**
- `200`: Successful Response
  Returns: `SetupStatusResponse`

---

## Share

### GET /share/{slug}
Get Public Agent

Public endpoint: Get agent info for the demo page. No auth required.

**Parameters:**
- `slug` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `PublicAgentResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Stats

### GET /stats
Get Dashboard Stats

Get dashboard statistics for the current tenant.

Returns aggregated stats including:
- Total calls this month
- Total minutes used this month
- Number of active agents
- Conversion rate (calls that booked appointments)
- Last 5 recent calls
- 7-day usage trend

**Responses:**
- `200`: Successful Response
  Returns: `DashboardStats`

---

### GET /stats/analytics
Get Analytics

Get analytics data for the interactive dashboard.

Returns summary stats, daily call volume trends, status/direction
breakdowns, and per-agent performance — all in one response.

**Parameters:**
- `date_from` (query, string | null) — Start date (YYYY-MM-DD)
- `date_to` (query, string | null) — End date (YYYY-MM-DD)
- `agent_id` (query, string | null) — Filter by agent ID

**Responses:**
- `200`: Successful Response
  Returns: `AnalyticsResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Tenants

### GET /tenants/me
Get Current Tenant

Get current tenant details with usage stats.

**Responses:**
- `200`: Successful Response
  Returns: `TenantDetailResponse`

---

### PATCH /tenants/me
Update Tenant

Update current tenant settings.

Uses get_effective_tenant_id so agency owners editing a sub-account's
settings (webhook, etc.) write to the sub-account, not the parent.

**Request Body:** `TenantUpdate` (application/json)
- name: string | null
- webhook_url: string | null
- webhook_enabled: boolean | null
- ghl_conversation_sync_enabled: boolean | null

**Responses:**
- `200`: Successful Response
  Returns: `TenantResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /tenants/me/webhook
Get Webhook Settings

Get webhook configuration for the effective tenant (sub-account aware).

**Responses:**
- `200`: Successful Response
  Returns: `WebhookSettingsResponse`

---

### POST /tenants/me/webhook-test
Test Webhook

Send a test payload to the configured webhook URL (sub-account aware).

**Responses:**
- `200`: Successful Response

---

## Test

### GET /test/active-sessions
List Active Sessions

List active voice sessions (for testing).

**Responses:**
- `200`: Successful Response

---

### POST /test/kill-xai/{call_sid}
Kill Xai Connection

Kill xAI connection to test graceful degradation.

**Parameters:**
- `call_sid` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Testing

### GET /testing/agents/{agent_id}/analysis-history
Get Analysis History

Get historical diagnosis scores for an agent, for trend charting.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/analyze-calls
Analyze Calls

Analyze one or more call transcripts with custom criteria.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `AnalyzeCallsRequest` (application/json)
- call_ids: array of string (required)
- criteria: array of AnalysisCriterion
- model: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/analyze-calls-stream
Analyze Calls Stream

Analyze call transcripts with SSE streaming progress.

Returns Server-Sent Events:
- progress: {current, total, call_id, status}
- call_result: per-call analysis result
- call_error: per-call error
- complete: final summary
- error: fatal error

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `AnalyzeCallsRequest` (application/json)
- call_ids: array of string (required)
- criteria: array of AnalysisCriterion
- model: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/apply-prompt
Apply Prompt

Apply a prompt suggestion to the agent's system prompt.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `ApplyPromptRequest` (application/json)
- original_text: string (required)
- suggested_text: string (required)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/coaching-plan
Generate Coaching Plan

Generate a coaching plan from diagnosis findings.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** object (application/json)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/rewrite-prompt
Rewrite Prompt

Holistically rewrite the agent's prompt incorporating all suggestions. Returns preview.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `RewritePromptRequest` (application/json)
- suggestions: array of object (required) — List of suggestion objects from suggest-prompt
- model: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/save-rewritten-prompt
Save Rewritten Prompt

Save an approved rewritten prompt to the agent.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `SaveRewrittenPromptRequest` (application/json)
- rewritten_prompt: string (required)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/simulate
Run Simulation

Run a bot-vs-bot simulation against an agent. Returns immediately with running status.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `ScenarioRequest` (application/json)
- scenario_name: string | null
- persona: string | null
- description: string | null
- criteria: array of ScenarioCriterion
- judge_model: string
- simulator_model: string
- max_turns: integer

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /testing/agents/{agent_id}/simulations
Get Agent Simulations

List simulation runs for an agent.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /testing/agents/{agent_id}/suggest-prompt
Suggest Prompt

Generate prompt improvement suggestions from analysis/simulation results.

**Parameters:**
- `agent_id` (path, string (required))

**Request Body:** `SuggestPromptRequest` (application/json)
- analysis_ids: array of string — Call analysis IDs to base suggestions on
- simulation_id: string | null
- failures: array of object — Inline failure data: [{name, reasoning, call_summary}]
- model: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /testing/agents/{agent_id}/suggested-criteria
Get Agent Suggested Criteria

Return criteria relevant to this agent's enabled tools and feature flags.

**Parameters:**
- `agent_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /testing/byok-keys
Get Byok Keys

List all BYOK keys for the current tenant (no secrets returned).

**Responses:**
- `200`: Successful Response

---

### POST /testing/byok-keys
Create Key

Add a new BYOK key. Validates the key before storing.

**Request Body:** `BYOKKeyCreate` (application/json)
- provider: string (required)
- api_key: string (required)
- label: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /testing/byok-keys/{provider}
Remove Key

Delete a BYOK key.

**Parameters:**
- `provider` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /testing/criteria-library
Get Criteria Library

Return the full criteria library with categories. Static data, cacheable.

**Responses:**
- `200`: Successful Response

---

### POST /testing/generate-scenario
Generate Scenario

Generate a simulation scenario from a natural language description using AI.

**Request Body:** `GenerateScenarioRequest` (application/json)
- description: string (required) — Natural language scenario description
- model: string

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /testing/scenarios
Get Scenarios

List available pre-built scenarios.

**Responses:**
- `200`: Successful Response

---

### GET /testing/simulations/{run_id}
Get Simulation

Get a simulation run by ID (poll for completion).

**Parameters:**
- `run_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Text-Assistants

### GET /text-assistants
List Text Assistants

List all text assistants for the current tenant.

**Responses:**
- `200`: Successful Response
  Returns: `TextAssistantListResponse`

---

### POST /text-assistants
Create Text Assistant

Create a new text assistant.

**Request Body:** `TextAssistantCreate` (application/json)
- name: string (required)
- agent_id: string (required) — Link to a voice agent. Required - inherits prompt and functions from agent.
- active_tag: string | null — GHL contact tag that activates this assistant
- mode: string
- business_hours: object | null
- timezone: string
- enabled_channels: EnabledChannels | null
- human_takeover_timeout_hours: integer
- delayed_trigger_enabled: boolean
- schedule_text_back_enabled: boolean
- ghl_integration_id: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- text_model: string — AI model for text message responses

**Responses:**
- `201`: Successful Response
  Returns: `TextAssistantResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /text-assistants/wizard/defaults
Get Wizard Defaults

Get default settings for the text assistant wizard.

Returns recommended settings for a text assistant.

**Responses:**
- `200`: Successful Response
  Returns: `TextDefaultsResponse`

---

### POST /text-assistants/wizard/enhance-description
Enhance Description

Enhance a basic business description using AI.

Takes a rough description and makes it more polished and professional
while keeping it concise (under 50 words).

**Request Body:** `EnhanceDescriptionRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- description: string (required)

**Responses:**
- `200`: Successful Response
  Returns: `EnhanceDescriptionResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /text-assistants/wizard/generate-all-knowledge
Generate All Knowledge Endpoint

Generate all knowledge sections at once.

This is a convenience endpoint that generates services, pricing,
team, and FAQs in a single call. Takes longer but provides
everything needed for the assistant prompt.

**Request Body:** `app__text_assistant__prompt_router__GenerateAllKnowledgeRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- description: string — Business description for context

**Responses:**
- `200`: Successful Response
  Returns: `GenerateAllKnowledgeResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /text-assistants/wizard/generate-knowledge
Generate Knowledge

Generate AI suggestions for a specific knowledge section.

This endpoint uses xAI to generate content for one section at a time,
allowing users to iterate on each section individually.

**Sections:**
- `services`: Products and services offered
- `pricing`: Pricing information
- `team`: Team members and roles
- `faqs`: Common questions and answers

**Request Body:** `app__text_assistant__prompt_router__GenerateKnowledgeRequest` (application/json)
- business_name: string (required)
- industry: string (required)
- section: string (required) — Section to generate: services, pricing, team, or faqs
- description: string — Business description for context
- services: string — Existing services list (for pricing/faqs context)

**Responses:**
- `200`: Successful Response
  Returns: `GenerateKnowledgeResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /text-assistants/wizard/industry-presets
Get Industry Presets

Get available industry presets.

Returns a list of supported industries and their associated
suggestions for services and FAQs.

**Responses:**
- `200`: Successful Response
  Returns: `IndustryPresetsResponse`

---

### POST /text-assistants/wizard/preview-prompt
Preview Prompt

Preview the full generated prompt before creating the text assistant.

This builds the complete text assistant prompt from the provided
knowledge sections and returns it along with recommended settings.

**Request Body:** `TextPreviewPromptRequest` (application/json)
- business_name: string (required)
- assistant_name: string
- industry: string
- description: string
- services: string
- pricing: string
- team: string
- faqs: string

**Responses:**
- `200`: Successful Response
  Returns: `TextPreviewPromptResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /text-assistants/{assistant_id}
Get Text Assistant

Get a specific text assistant.

**Parameters:**
- `assistant_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `TextAssistantResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### PATCH /text-assistants/{assistant_id}
Update Text Assistant

Update a text assistant.

**Parameters:**
- `assistant_id` (path, string (required))

**Request Body:** `TextAssistantUpdate` (application/json)
- name: string | null
- agent_id: string | null
- is_active: boolean | null
- active_tag: string | null — GHL contact tag that activates this assistant
- mode: string | null
- business_hours: object | null
- timezone: string | null
- enabled_channels: EnabledChannels | null
- human_takeover_timeout_hours: integer | null
- delayed_trigger_enabled: boolean | null
- schedule_text_back_enabled: boolean | null
- ghl_integration_id: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- text_model: string | null
- followup_config: object | null

**Responses:**
- `200`: Successful Response
  Returns: `TextAssistantResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### DELETE /text-assistants/{assistant_id}
Delete Text Assistant

Delete a text assistant.

**Parameters:**
- `assistant_id` (path, string (required))

**Responses:**
- `204`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /text-assistants/{assistant_id}/send
Send Outbound Text

Send an outbound text message via this assistant.

**Parameters:**
- `assistant_id` (path, string (required))

**Request Body:** `OutboundTextSendRequest` (application/json)
- phone_number: string | null
- ghl_contact_id: string | null
- message: string | null
- ai_generate: boolean
- ai_context: string | null
- channel: string

**Responses:**
- `200`: Successful Response
  Returns: `OutboundTextSendResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /text-assistants/{assistant_id}/tag-contact-count
Get Tag Contact Count

Get the count of GHL contacts with this assistant's active tag.

**Parameters:**
- `assistant_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /text-assistants/{assistant_id}/toggle
Toggle Text Assistant

Toggle text assistant active status.

**Parameters:**
- `assistant_id` (path, string (required))

**Responses:**
- `200`: Successful Response
  Returns: `TextAssistantResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Text-Followup

### GET /text-followup/activity
List Activity

List follow-up activity for the monitoring page.

**Parameters:**
- `limit` (query, integer)
- `offset` (query, integer)
- `status` (query, string | null)

**Responses:**
- `200`: Successful Response
  Returns: `FollowUpActivityResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /text-followup/activity/{job_id}/cancel
Cancel Job

Manually cancel a pending follow-up job.

**Parameters:**
- `job_id` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Tools

### POST /tools/scrape-website
Scrape Website Endpoint

Scrape a website and extract structured business information.

Uses Jina Reader for scraping and xAI for AI extraction.

**Request Body:** `ScrapeWebsiteRequest` (application/json)
- url: string (required) — Website URL to scrape

**Responses:**
- `200`: Successful Response
  Returns: `ScrapeWebsiteResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /tools/screenshot
Screenshot Endpoint

Capture a website screenshot and upload to storage.

Uses ScreenshotOne API for capture and Supabase Storage for hosting.

**Request Body:** `ScreenshotRequest` (application/json)
- url: string (required) — Website URL to screenshot
- width: integer
- height: integer
- full_page: boolean

**Responses:**
- `200`: Successful Response
  Returns: `ScreenshotResponse`
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Voice-Samples

### GET /voice-samples/
List Voice Samples

List all available voice samples.

Returns:
    List of available voice names with URLs

**Responses:**
- `200`: Successful Response

---

### GET /voice-samples/gemini/{voice}.mp3
Get Gemini Voice Sample

Serve pre-generated Gemini voice sample MP3.

**Parameters:**
- `voice` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /voice-samples/openai/{voice}.mp3
Get Openai Voice Sample

Serve pre-generated OpenAI voice sample MP3.

**Parameters:**
- `voice` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /voice-samples/premium/{voice}.mp3
Get Premium Voice Sample

Serve pre-generated ElevenLabs voice sample MP3.

**Parameters:**
- `voice` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /voice-samples/{voice}.mp3
Get Voice Sample

Serve pre-generated Standard voice sample MP3.

**Parameters:**
- `voice` (path, string (required))

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

## Webhooks

### GET /webhooks/events
List Webhook Events

Return a manifest of all supported webhook event types with payload schemas.

Requires authentication (session or API key).

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/ghl/app-install
Handle App Install

Handle GHL AppInstall webhook (marketplace lifecycle).

NOTE: GHL marketplace lifecycle webhooks do NOT include signature headers,
so this endpoint does not use verify_ghl_signature. This is expected
GHL behavior — only conversation/message webhooks are signed.

Logs the install event and reactivates existing integrations if found.
New integrations are NOT created here — the existing OAuth flow handles
creating the integration record with proper tenant_id and tokens.

Always returns 200 to prevent GHL retries.

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/ghl/app-uninstall
Handle App Uninstall

Handle GHL AppUninstall webhook (marketplace lifecycle).

NOTE: GHL marketplace lifecycle webhooks do NOT include signature headers,
so this endpoint does not use verify_ghl_signature. This is expected
GHL behavior — only conversation/message webhooks are signed.

Deactivates the integration for the uninstalled location.

Always returns 200 to prevent GHL retries.

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/ghl/conversations
Handle Ghl Message

Handle GHL InboundMessage webhooks.

Flow:
1. Verify webhook signature
2. Find tenant by GHL location
3. Check if AI should respond
4. Add to debounce queue
5. Return 200 immediately

Note: Always return 200 to prevent GHL retries.

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/ghl/conversations/human-takeover
Handle Human Takeover

Handle OutboundMessage webhooks to detect human staff replies.

When a human staff member sends a message, pause AI for that conversation.

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/stripe
Handle Stripe Webhook

Handle incoming Stripe webhook events.

Security checks (in order):
1. Verify signature header exists
2. Verify webhook secret is configured
3. Validate timestamp (CRIT-005 - replay protection)
4. Verify signature using Stripe SDK
5. Check deduplication (CRIT-003 - idempotency)
6. Validate required fields (CRIT-004)
7. Process event

**Responses:**
- `200`: Successful Response

---

### POST /webhooks/twilio/{tenant_id}/amd-status
Handle Amd Status

Handle AMD (Answering Machine Detection) results from Twilio.

Called asynchronously by Twilio when AMD determines whether a human
or machine answered the outbound call.

AnsweredBy values:
- human: A person answered
- machine_start: Voicemail detected (haven't waited for beep)
- machine_end_beep: Voicemail beep detected
- machine_end_silence: Voicemail silence detected
- machine_end_other: Voicemail ended another way
- fax: Fax machine detected
- unknown: Unable to determine

Based on agent's amd_voicemail_behavior, we either:
- hangup: Immediately end the call
- static_message: Play pre-configured voicemail message
- dynamic_message: Play message with {{variable}} substitution
- agent_decides: Let the AI agent handle it (no action here)

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/recording
Handle Recording Ready

Handle recording completion callback from Twilio.

Updates the call log with the recording URL.

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/sms
Handle Incoming Sms

Handle inbound SMS/MMS from Twilio.

MMS attachments (images, voice notes) are extracted from the variable-count
MediaUrl{N}/MediaContentType{N} form fields Twilio sends and passed to
_process_incoming_sms for analysis via platform OpenAI key. Voice-only
MMS (empty Body + audio attachment) are processed after transcription.

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/sms-status
Handle Sms Status Callback

Twilio status callback for SMS pool sends.

Pool sends include a per-message status_callback URL that routes Twilio's
queued → sent → delivered/failed transitions back to us. Each callback
carries the pool_member_id in the query string so we can attribute stats
to the right pool member without secondary lookups.

Returns 204 on success (or duplicate); 403 on bad signature (handled by
the validate_twilio_signature dependency).

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/status
Handle Call Status

Handle call status updates from Twilio.

Updates the call log with status changes and duration when call completes.

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/voice
Handle Incoming Voice

Handle voice calls from Twilio (both inbound and outbound).

For inbound: Twilio calls us when someone dials our number
For outbound: Twilio calls us after we initiate via REST API

Returns TwiML to connect the call to our Media Streams WebSocket.

**Parameters:**
- `tenant_id` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### GET /webhooks/twilio/{tenant_id}/whisper/{call_sid}
Handle Whisper

Serve whisper TwiML to Twilio when transfer recipient answers.

Generates a 2-3 sentence AI summary of the call transcript and returns
it as <Say> TwiML. Falls back to empty response on any error.

**Parameters:**
- `tenant_id` (path, string (required))
- `call_sid` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---

### POST /webhooks/twilio/{tenant_id}/whisper/{call_sid}
Handle Whisper

Serve whisper TwiML to Twilio when transfer recipient answers.

Generates a 2-3 sentence AI summary of the call transcript and returns
it as <Say> TwiML. Falls back to empty response on any error.

**Parameters:**
- `tenant_id` (path, string (required))
- `call_sid` (path, string (required))
- `x-twilio-signature` (header, string | null)

**Responses:**
- `200`: Successful Response
- `422`: Validation Error
  Returns: `HTTPValidationError`

---


# Schemas

Component models referenced by request/response shapes above.

---

## APIKeyCreate

Request to create a new API key.

**Fields:**
- name: string
- expires_in_days: integer | null

---

## APIKeyCreateResponse

Response after creating an API key (includes plaintext key ONCE).

**Fields:**
- id: string (required)
- name: string (required)
- key_prefix: string (required)
- plaintext_key: string (required)
- created_at: string (required)
- expires_at: string | null

---

## APIKeyListResponse

List of API keys.

**Fields:**
- keys: array of APIKeyResponse (required)
- total: integer (required)

---

## APIKeyResponse

API key response (without the actual key).

**Fields:**
- id: string (required)
- name: string (required)
- key_prefix: string (required)
- created_at: string (required)
- last_used_at: string | null
- is_active: boolean
- expires_at: string | null

---

## AcceptInviteRequest

Request body for accepting a sub-account invite.

**Fields:**
- token: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)

---

## AcceptOutboundTermsRequest

Request: accept outbound calling terms.

**Fields:**
- terms_version: string

---

## AdminDashboardResponse

Aggregated admin dashboard metrics.

**Fields:**
- stripe: SourceMetrics (required)
- sentry: SourceMetrics (required)
- ga4: SourceMetrics (required)
- meta: SourceMetrics (required)
- render: SourceMetrics (required)
- twilio: SourceMetrics (required)
- xai: SourceMetrics (required)
- elevenlabs: SourceMetrics (required)
- gemini: SourceMetrics (required)
- openai: SourceMetrics (required)
- user_stats: object (required)

---

## AffiliateCodeResponse

Response containing affiliate code and URL.

**Fields:**
- affiliate_code: string (required)
- affiliate_url: string (required)

---

## AffiliateReferral

Single referral record with commission info.

**Fields:**
- id: string (required)
- referred_tenant_name: string (required)
- subscription_plan: string | null (required)
- commission_cents: integer (required)
- status: string (required)
- created_at: string (required)

---

## AffiliateStatsResponse

Complete affiliate dashboard data.

**Fields:**
- affiliate_code: string (required)
- affiliate_url: string (required)
- total_referrals: integer (required)
- active_referrals: integer (required)
- total_earned_cents: integer (required)
- pending_payout_cents: integer (required)
- referrals: array of AffiliateReferral (required)

---

## AgencyIntegrationsResponse

List of agency's integrations available for assignment.

**Fields:**
- integrations: array of IntegrationInfo (required)
- total_count: integer (required)

---

## AgencyOverview

Agency dashboard overview stats.

**Fields:**
- total_sub_accounts: integer (required)
- active_sub_accounts: integer (required)
- suspended_sub_accounts: integer (required)
- total_agents: integer (required)
- total_calls: integer (required)
- total_minutes: number (required)
- total_texts: integer
- total_margin_cents: integer (required)
- total_revenue_cents: integer
- total_cost_cents: integer
- avg_margin_pct: number
- total_booked: integer
- conversion_rate: number
- calls_by_direction: object
- top_sub_accounts: array of app__agency__schemas__SubAccountSummary
- daily_trend: array of DailyAgencyTrend
- usage_by_provider: array of ProviderBreakdown

---

## AgentBreakdown

Per-agent aggregated stats.

**Fields:**
- agent_id: string (required)
- agent_name: string (required)
- calls: integer
- minutes: number
- booked: integer
- conversion_rate: number

---

## AgentCreate

Request body for creating an agent.

**Fields:**
- name: string (required)
- system_prompt: string (required)
- greeting: string | null
- greeting_outbound: string | null
- voice: string
- temperature: number
- business_name: string | null
- industry: string | null
- ghl_phone_number: string | null
- calendar_provider: string | null — Calendar provider: 'gohighlevel'
- calendar_integration_id: string | null — Which GHL integration to use (for multi-account support)
- calendar_id: string | null — Calendar ID from provider
- tools_enabled: array of string | null — List of enabled tool names (e.g., ['end_call', 'book_appointment'])
- timezone: string — IANA timezone (e.g., America/New_York, America/Los_Angeles)
- vad_threshold: number — VAD sensitivity (0.0-1.0, higher = less sensitive)
- vad_silence_duration_ms: integer — Silence duration before ending turn (ms)
- vad_prefix_padding_ms: integer — Audio capture before speech detection (ms)
- enable_web_search: boolean — Enable web search capability
- enable_x_search: boolean — Enable X (Twitter) search
- x_search_handles: array of string | null — Allowed X handles for search (e.g., ['elonmusk', 'xai'])
- enable_collections_search: boolean — Enable document search from tenant knowledge base
- knowledge_base_ids: array of string — Knowledge Base IDs this agent can search (when enable_collections_search=true)
- enable_recording_disclosure: boolean — Announce call recording at start of calls (required for two-party consent states)
- recording_enabled: boolean — When true, defer GHL conversation sync and post-call webhook to recording.ready so the Twilio recording URL is included.
- enable_contact_intelligence: boolean — Fetch caller context (GHL contact + call history) before answering
- ai_speaks_first: boolean — If true, AI greets caller immediately. If false, AI waits for caller to speak first.
- ai_speaks_first_outbound: boolean — If true, AI greets recipient immediately on outbound calls.
- finish_greeting_before_listening: boolean — If true, caller cannot interrupt the agent's first response (inbound). Ignored if ai_speaks_first is false — validator w
- finish_greeting_before_listening_outbound: boolean — If true, recipient cannot interrupt the agent's first response on outbound calls. Ignored if ai_speaks_first_outbound is
- prompt_includes_contact_intelligence: boolean — True if prompt includes Caller Intelligence section for using pre-call context
- voice_provider: string — Voice provider: 'xai' (Grok), 'elevenlabs' (ElevenLabs), 'openai' (OpenAI), or 'gemini' (Gemini)
- gemini_voice: string — Gemini prebuilt voice name (30 options)
- gemini_start_sensitivity: string — Gemini start-of-speech sensitivity: low (ignores noise) or high (reacts to everything)
- gemini_end_sensitivity: string — Gemini end-of-speech sensitivity: low (patient, waits for clear silence) or high (quick cutoff). WARNING: LOW on 8kHz te
- gemini_thinking_level: string — Gemini 3.1 thinking level: none (off, fastest), minimal (very light), low (basic reasoning), medium, high (most thorough
- gemini_language_code: string | null — BCP-47 language code hint for Gemini speech (e.g., 'en-US', 'es-US', 'fr-FR'). None = auto-detect.
- gemini_affective_dialog: boolean — Enable emotion/tone awareness in Gemini responses (Preview feature)
- gemini_proactive_audio: boolean — Allow Gemini to stay silent when no clear request is made (Preview feature)
- gemini_top_k: integer | null — Gemini top-K sampling: number of top tokens considered (1-100, None=model default)
- gemini_top_p: number | null — Gemini top-P nucleus sampling threshold (0.0-1.0, None=model default)
- openai_voice: string — OpenAI voice ID. v1.5 voices: alloy, ash, ballad, coral, echo, sage, shimmer, verse. v2 adds: marin, cedar (only availab
- openai_vad_type: string — OpenAI VAD type: semantic_vad (AI-based) or server_vad (volume-based)
- openai_vad_eagerness: string — OpenAI semantic VAD eagerness: low (patient) to high (responsive)
- openai_noise_reduction: string — OpenAI noise reduction: far_field (phone), near_field (mic), or disabled
- openai_voice_model: string — OpenAI Realtime model version. v1.5 is the default audio model; v2 adds reasoning at premium pricing.
- openai_reasoning_effort: string — Reasoning effort for gpt-realtime-2. Ignored on v1.5. Default 'low' is recommended for production voice.
- elevenlabs_voice_id: string | null — ElevenLabs voice ID
- elevenlabs_model_id: string — LLM model ID for ElevenLabs agent (e.g., claude-sonnet-4-5, gpt-4o-mini, claude-3-haiku)
- elevenlabs_speed: number — Speaking speed for ElevenLabs (0.7-1.2x)
- elevenlabs_eagerness: string — Turn-taking eagerness for ElevenLabs: 'low', 'normal', or 'high'
- elevenlabs_language: string — Language code for ElevenLabs agent (e.g., 'en', 'es', 'fr')
- elevenlabs_additional_languages: array of string — Additional language codes for multilingual support (e.g., ['es', 'fr'])
- elevenlabs_stability: number — Voice stability for ElevenLabs (0.0=creative, 0.5=natural, 1.0=robust)
- elevenlabs_max_duration_seconds: integer | null — Max call duration in seconds for ElevenLabs (None=unlimited, min 60)
- elevenlabs_emotion_tags: array of object | null — Custom emotion tags for ElevenLabs: [{name, description}]
- elevenlabs_tool_call_sound: string | null — Sound played during ElevenLabs tool execution: typing, elevator1-4, none
- elevenlabs_pre_tool_speech: boolean | null — Agent announces action before executing slow tools (ElevenLabs only)
- xai_audio_tags: array of string | null — xAI audio delivery tags: ['[breath]', '[pause]', '<whisper>', ...]
- agent_mode: string — How this agent handles calls: 'inbound', 'outbound', or 'both'
- voice_enabled: boolean — Enable voice/phone channel
- text_enabled: boolean — Enable text/SMS channel
- amd_enabled: boolean — Enable Twilio AMD for outbound calls ($0.01/call)
- amd_voicemail_behavior: string — Action when voicemail detected: hangup, static_message, dynamic_message, agent_decides
- amd_voicemail_message: string | null — Message to leave on voicemail (supports {{variables}} for dynamic_message)
- amd_voicemail_audio_url: string | null — Audio file URL to play as voicemail (alternative to TTS)
- transfer_targets: array of object | null — Transfer targets: [{name, number, reason}]
- whisper_enabled: boolean — Enable AI-generated whisper summary when transferring calls
- ghl_tags: array of object | null — Available tags for GHL add_tag/remove_tag: [{name}]
- ghl_remove_tags: array of object | null — Tag rules for remove_tag: [{name, condition?}]
- ghl_workflows: array of object | null — Available workflows for GHL trigger_workflow: [{id, name, description?}]
- ghl_pipelines: array of object | null — Available pipelines for GHL opportunities: [{id, name, stages: [{id, name}]}]
- sms_templates: array of object | null — SMS templates for send_sms: [{name, content}]
- sms_phone_number_id: string | null — Phone number ID to use for send_sms tool (overrides agent's voice number)
- max_call_duration_minutes: integer — Max call duration in minutes (0=unlimited, max 180)
- max_silence_seconds: integer — Max silence before ending call in seconds (0=unlimited, max 600)
- calendar_configs: array of object | null — Calendar configurations: [{calendar_id, integration_id, label, provider}]
- multi_calendar_behavior: string — Multi-calendar behavior: 'ask_user' (present options) or 'auto_first' (book first available)
- variable_definitions: array of VariableDefinition | null — Template variables for prompt substitution: [{name, description?, required?, default_value?}]
- tool_instructions: object | null — Per-tool usage instructions: {"tool_name": "instruction text"}
- text_model: string — LLM model for text assistant (claude-haiku-4-5-20251001, claude-sonnet-4-6, claude-sonnet-4-5-20250929, claude-opus-4-6,
- channel_pivot_enabled: boolean — Auto-send text when outbound call fails (no-answer, busy, voicemail)
- mcp_servers: array of MCPServerConfig | null

---

## AgentFunctionResponse

Response schema for a function attached to a specific agent.

**Fields:**
- id: string (required)
- function_id: string (required)
- agent_id: string (required)
- is_enabled: boolean (required)
- created_at: string (required)
- function: CustomFunctionResponse (required)

---

## AgentFunctionsListResponse

Response for listing functions attached to an agent plus available library functions.

**Fields:**
- attached: array of AgentFunctionResponse — Functions attached to this agent
- available: array of CustomFunctionResponse — Library functions not yet attached to this agent
- total_attached: integer
- total_available: integer

---

## AgentListResponse

List of agents response.

**Fields:**
- agents: array of AgentResponse (required)
- total: integer (required)

---

## AgentResponse

Agent data response.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- name: string (required)
- is_active: boolean (required)
- voice: string (required)
- temperature: number (required)
- business_name: string | null
- industry: string | null
- system_prompt: string | null
- greeting: string | null
- greeting_outbound: string | null
- ghl_phone_number: string | null
- calendar_provider: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- tools_enabled: array of string | null
- timezone: string | null
- vad_threshold: number | null
- vad_silence_duration_ms: integer | null
- vad_prefix_padding_ms: integer | null
- enable_web_search: boolean | null
- enable_x_search: boolean | null
- x_search_handles: array of string | null
- enable_collections_search: boolean | null
- knowledge_base_ids: array of string | null
- enable_recording_disclosure: boolean | null
- recording_enabled: boolean | null
- enable_contact_intelligence: boolean | null
- ai_speaks_first: boolean | null
- ai_speaks_first_outbound: boolean | null
- finish_greeting_before_listening: boolean | null
- finish_greeting_before_listening_outbound: boolean | null
- prompt_includes_contact_intelligence: boolean | null
- voice_provider: string | null
- gemini_voice: string | null
- gemini_start_sensitivity: string | null
- gemini_end_sensitivity: string | null
- gemini_thinking_level: string | null
- gemini_language_code: string | null
- gemini_affective_dialog: boolean | null
- gemini_proactive_audio: boolean | null
- gemini_top_k: integer | null
- gemini_top_p: number | null
- openai_voice: string | null
- openai_vad_type: string | null
- openai_vad_eagerness: string | null
- openai_noise_reduction: string | null
- openai_voice_model: string | null
- openai_reasoning_effort: string | null
- elevenlabs_voice_id: string | null
- elevenlabs_model_id: string | null
- elevenlabs_speed: number | null
- elevenlabs_eagerness: string | null
- elevenlabs_language: string | null
- elevenlabs_additional_languages: array of string | null
- elevenlabs_stability: number | null
- elevenlabs_max_duration_seconds: integer | null
- elevenlabs_emotion_tags: array of object | null
- elevenlabs_agent_id: string | null
- elevenlabs_tool_call_sound: string | null
- elevenlabs_pre_tool_speech: boolean | null
- xai_audio_tags: array of string | null
- agent_mode: string | null
- voice_enabled: boolean
- text_enabled: boolean
- amd_enabled: boolean | null
- amd_voicemail_behavior: string | null
- amd_voicemail_message: string | null
- amd_voicemail_audio_url: string | null
- transfer_targets: array of object | null
- whisper_enabled: boolean | null
- ghl_tags: array of object | null
- ghl_remove_tags: array of object | null
- ghl_workflows: array of object | null
- ghl_pipelines: array of object | null
- sms_templates: array of object | null
- sms_phone_number_id: string | null
- max_call_duration_minutes: integer | null
- max_silence_seconds: integer | null
- calendar_configs: array of object | null
- multi_calendar_behavior: string | null
- variable_definitions: array of VariableDefinition | null
- tool_instructions: object | null
- text_model: string | null
- channel_pivot_enabled: boolean | null
- phone_count: integer
- text_assistants: array of LinkedTextAssistantSummary
- mcp_servers: array of MCPServerSummary
- created_at: string (required)
- updated_at: string (required)

---

## AgentSummary

Agent summary for user detail.

**Fields:**
- id: string (required)
- name: string (required)
- is_active: boolean (required)
- created_at: string (required)

---

## AgentUpdate

Request body for updating an agent.

**Fields:**
- name: string | null
- system_prompt: string | null
- greeting: string | null
- greeting_outbound: string | null
- voice: string | null
- temperature: number | null
- is_active: boolean | null
- business_name: string | null
- industry: string | null
- ghl_phone_number: string | null
- calendar_provider: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- tools_enabled: array of string | null
- timezone: string | null
- vad_threshold: number | null
- vad_silence_duration_ms: integer | null
- vad_prefix_padding_ms: integer | null
- enable_web_search: boolean | null
- enable_x_search: boolean | null
- x_search_handles: array of string | null
- enable_collections_search: boolean | null
- knowledge_base_ids: array of string | null
- enable_recording_disclosure: boolean | null
- recording_enabled: boolean | null
- enable_contact_intelligence: boolean | null
- ai_speaks_first: boolean | null
- ai_speaks_first_outbound: boolean | null
- finish_greeting_before_listening: boolean | null
- finish_greeting_before_listening_outbound: boolean | null
- prompt_includes_contact_intelligence: boolean | null
- voice_provider: string | null — Voice provider: 'xai' (Grok), 'elevenlabs' (ElevenLabs), 'openai' (OpenAI), or 'gemini' (Gemini)
- gemini_voice: string | null
- gemini_start_sensitivity: string | null
- gemini_end_sensitivity: string | null
- gemini_thinking_level: string | null
- gemini_language_code: string | null
- gemini_affective_dialog: boolean | null
- gemini_proactive_audio: boolean | null
- gemini_top_k: integer | null
- gemini_top_p: number | null
- openai_voice: string | null
- openai_vad_type: string | null
- openai_vad_eagerness: string | null
- openai_noise_reduction: string | null
- openai_voice_model: string | null
- openai_reasoning_effort: string | null
- elevenlabs_voice_id: string | null
- elevenlabs_model_id: string | null
- elevenlabs_speed: number | null
- elevenlabs_eagerness: string | null
- elevenlabs_language: string | null
- elevenlabs_additional_languages: array of string | null
- elevenlabs_stability: number | null
- elevenlabs_max_duration_seconds: integer | null
- elevenlabs_emotion_tags: array of object | null
- elevenlabs_tool_call_sound: string | null
- elevenlabs_pre_tool_speech: boolean | null
- xai_audio_tags: array of string | null
- agent_mode: string | null — How this agent handles calls
- voice_enabled: boolean | null
- text_enabled: boolean | null
- amd_enabled: boolean | null
- amd_voicemail_behavior: string | null
- amd_voicemail_message: string | null
- amd_voicemail_audio_url: string | null
- transfer_targets: array of object | null
- whisper_enabled: boolean | null
- ghl_tags: array of object | null
- ghl_remove_tags: array of object | null
- ghl_workflows: array of object | null
- ghl_pipelines: array of object | null
- sms_templates: array of object | null
- sms_phone_number_id: string | null
- max_call_duration_minutes: integer | null
- max_silence_seconds: integer | null
- calendar_configs: array of object | null
- multi_calendar_behavior: string | null
- variable_definitions: array of VariableDefinition | null
- tool_instructions: object | null
- text_model: string | null
- channel_pivot_enabled: boolean | null
- mcp_servers: array of MCPServerConfig | null

---

## AllSubAccountAgentsResponse

All agents across all sub-accounts (for agency overview).

**Fields:**
- agents: array of SubAccountAgentInfo (required)
- total: integer (required)

---

## AllSubAccountFunctionsResponse

All custom functions across all sub-accounts (for agency sharing UI).

**Fields:**
- functions: array of SubAccountFunctionInfo (required)
- total: integer (required)

---

## AnalysisCriterion

**Fields:**
- name: string (required)
- description: string (required)

---

## AnalyticsKPIs

KPI counts for analytics dashboard.

**Fields:**
- total_users: integer (required)
- active_24h: integer (required)
- active_7d: integer (required)
- at_risk_count: integer (required)

---

## AnalyticsResponse

Single response for the analytics dashboard.

**Fields:**
- summary: AnalyticsSummary (required)
- daily_trend: array of DailyTrend (required)
- status_breakdown: array of StatusBreakdown (required)
- direction_breakdown: array of DirectionBreakdown (required)
- agent_breakdown: array of AgentBreakdown (required)

---

## AnalyticsSummary

Totals for the selected period.

**Fields:**
- total_calls: integer
- total_minutes: number
- total_cost_cents: integer
- conversion_rate: number
- total_texts: integer

---

## AnalyzeCallsRequest

Analyze one or more call transcripts. Empty criteria triggers diagnosis mode.

**Fields:**
- call_ids: array of string (required)
- criteria: array of AnalysisCriterion
- model: string

---

## ApplyCouponRequest

Request to apply a promotion code to an existing subscription.

**Fields:**
- promotion_code: string (required)

---

## ApplyCouponResponse

Response after applying a coupon.

**Fields:**
- success: boolean (required)
- discount_description: string (required)

---

## ApplyPromptRequest

Apply a suggestion to the agent's system prompt.

**Fields:**
- original_text: string (required)
- suggested_text: string (required)

---

## Appointment

Schema for a single GHL calendar appointment.

**Fields:**
- id: string (required)
- calendar_id: string (required)
- calendar_name: string | null
- contact_id: string | null
- contact_name: string | null
- contact_phone: string | null
- title: string | null
- start_time: string (required)
- end_time: string | null
- status: string (required)
- notes: string | null

---

## AppointmentEntry

A single appointment entry from GHL.

**Fields:**
- datetime: string (required)
- appointment_id: string (required)

---

## AppointmentsResponse

Response schema for appointments list endpoint.

**Fields:**
- appointments: array of Appointment (required)
- total: integer (required)
- has_more: boolean (required)
- integration_id: string | null

---

## AssignIntegrationResponse

Response after assigning integration to sub-account.

**Fields:**
- success: boolean (required)
- sub_account_id: string (required)
- integration_id: string (required)
- provider: string (required)
- account_name: string | null

---

## AssignIntegrationsRequest

Request to assign multiple integrations to a sub-account.

**Fields:**
- integration_ids: array of string (required)

---

## AssignIntegrationsResponse

Response after assigning multiple integrations to sub-account.

**Fields:**
- success: boolean (required)
- sub_account_id: string (required)
- assigned: array of AssignIntegrationResponse (required)
- errors: array of string

---

## AssignPhoneNumberRequest

Request to assign a phone number to a sub-account.

**Fields:**
- sub_account_id: string | null — Sub-account ID to assign to, or None to unassign

---

## AttachFunctionRequest

Request to attach a library function to an agent.

**Fields:**
- function_id: string (required) — ID of the function to attach
- is_enabled: boolean — Whether function is enabled for this agent

---

## AttachFunctionResponse

Response after attaching a function to an agent.

**Fields:**
- id: string (required)
- agent_id: string (required)
- function_id: string (required)
- is_enabled: boolean (required)
- created_at: string (required)

---

## AuthResponse

Full authentication response with tokens, user, and tenant.

**Fields:**
- access_token: string (required)
- refresh_token: string (required)
- token_type: string
- expires_in: integer (required)
- user: UserResponse (required)
- tenant: TenantResponse (required)

---

## BYOKKeyCreate

**Fields:**
- provider: string (required)
- api_key: string (required)
- label: string

---

## Body_create_issue_issues__post

**Fields:**
- message: string (required)
- url: string | null
- page_name: string | null
- browser_info: string | null
- image: string | null

---

## Body_handle_amd_status_webhooks_twilio__tenant_id__amd_status_post

**Fields:**
- CallSid: string (required)
- AnsweredBy: string (required)
- MachineDetectionDuration: string

---

## Body_handle_call_status_webhooks_twilio__tenant_id__status_post

**Fields:**
- CallSid: string (required)
- CallStatus: string (required)
- CallDuration: string | null

---

## Body_handle_incoming_sms_webhooks_twilio__tenant_id__sms_post

**Fields:**
- From: string (required)
- To: string (required)
- Body: string
- MessageSid: string (required)
- AccountSid: string
- NumMedia: string

---

## Body_handle_incoming_voice_webhooks_twilio__tenant_id__voice_post

**Fields:**
- CallSid: string (required)
- From: string (required)
- To: string (required)
- CallStatus: string
- Direction: string

---

## Body_handle_recording_ready_webhooks_twilio__tenant_id__recording_post

**Fields:**
- CallSid: string (required)
- RecordingUrl: string (required)
- RecordingDuration: string
- RecordingSid: string (required)

---

## Body_handle_sms_status_callback_webhooks_twilio__tenant_id__sms_status_post

**Fields:**
- MessageSid: string (required)
- MessageStatus: string (required)
- From: string
- To: string
- ErrorCode: string | null
- AccountSid: string

---

## Body_parse_csv_knowledge_bases__kb_id__tables_parse_csv_post

**Fields:**
- file: string (required)

---

## Body_upload_demo_image_demos__demo_id__upload_image_post

**Fields:**
- file: string (required)

---

## Body_upload_document_documents_post

**Fields:**
- file: string (required)
- description: string | null

---

## Body_upload_favicon_agency_branding_favicon_post

**Fields:**
- file: string (required)

---

## Body_upload_kb_document_knowledge_bases__kb_id__documents_post

**Fields:**
- file: string (required)
- description: string | null

---

## Body_upload_logo_agency_branding_logo_post

**Fields:**
- file: string (required)

---

## BrandingSettings

Agency branding settings.

**Fields:**
- company_name: string | null
- logo_url: string | null
- favicon_url: string | null
- primary_color: string
- support_email: string | null
- support_url: string | null

---

## BusinessHoursDay

Business hours configuration for a single day.

**Fields:**
- start: string
- end: string
- enabled: boolean

---

## CSVImportRequest

Bulk enrollment from CSV data.

**Fields:**
- rows: array of object (required) — Parsed CSV rows with mapped field names
- field_mapping: object (required) — CSV column → schema field mapping

---

## CSVImportResponse

**Fields:**
- enrolled: integer (required)
- skipped: integer (required)
- errors: array of object (required)

---

## CalendarInfo

Information about a calendar/event type.

**Fields:**
- id: string (required)
- name: string (required)
- provider: string (required)
- location_id: string | null
- duration_minutes: integer

---

## CallHistorySummary

Summary of a call for contact detail view.

**Fields:**
- id: string (required)
- direction: string (required)
- status: string (required)
- duration_seconds: integer | null
- started_at: string | null
- agent_name: string | null
- has_transcript: boolean
- summary: string | null
- sentiment: string | null
- caller_reason: string | null
- appointment_booked: boolean

---

## CallLogListResponse

Response schema for listing call logs.

**Fields:**
- calls: array of CallLogResponse (required)
- total: integer (required)

---

## CallLogResponse

Response schema for a call log entry.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- agent_id: string | null
- agent_name: string | null
- phone_number_id: string | null
- twilio_call_sid: string (required)
- direction: string enum ['inbound', 'outbound', 'test', 'demo'] (required)
- from_number: string (required)
- to_number: string (required)
- status: string (required)
- started_at: string (required)
- ended_at: string | null
- duration_seconds: integer | null
- billable_minutes: integer | null
- cost_cents: integer | null
- recording_url: string | null
- recording_duration_seconds: integer | null
- caller_name: string | null
- caller_email: string | null
- transcript: string | array of object | null
- metadata: object | null
- appointment_booked: boolean | null
- amd_status: string | null
- amd_detection_ms: integer | null
- voice_provider: string | null

---

## ChannelConfig

Per-channel configuration with optional account filtering.

When accounts is empty, responds to ALL accounts for that channel.
When accounts has values, only responds to those specific accounts.

**Fields:**
- enabled: boolean
- accounts: array of string

---

## ChartDataPoint

Single data point for charts.

**Fields:**
- date: string (required)
- value: number (required)

---

## ChatAssistantBreakdown

Per-assistant performance metrics.

**Fields:**
- assistant_id: string (required)
- assistant_name: string (required)
- conversations: integer
- messages: integer
- response_rate: number

---

## ChatDailyTrend

A single day's activity for the daily trend chart.

**Fields:**
- date: string (required)
- conversations: integer
- messages: integer
- ai_messages: integer

---

## ChatMessage

Single chat message in a conversation.

**Fields:**
- role: string enum ['user', 'assistant', 'system'] (required) — Message role
- content: string (required) — Message content

---

## ChatStatsResponse

Response schema for chat dashboard statistics.

**Fields:**
- total_conversations: integer
- total_messages: integer
- total_ai_messages: integer
- total_contact_messages: integer
- total_human_messages: integer
- actions_triggered: integer
- appointments_booked: integer
- active_conversations: integer
- channels: object
- time_saved_minutes: number
- response_rate: number
- avg_messages_per_conversation: number
- human_takeover_rate: number
- daily_trend: array of ChatDailyTrend
- assistant_breakdown: array of ChatAssistantBreakdown

---

## CheckSlugRequest

Request to check if a slug is available.

**Fields:**
- slug: string (required)

---

## CheckSlugResponse

Response for slug availability check.

**Fields:**
- available: boolean (required)
- slug: string (required)
- message: string | null

---

## CheckoutRequest

Request to create a Stripe Checkout session.

**Fields:**
- plan: string enum ['payg', 'starter', 'agency', 'pro'] (required)
- billing_period: string enum ['monthly', 'annual']
- success_url: string | null
- cancel_url: string | null

---

## CheckoutResponse

Response containing Stripe Checkout URL.

**Fields:**
- checkout_url: string (required)

---

## ChurnRiskUser

User at risk of churn.

**Fields:**
- id: string (required)
- email: string (required)
- full_name: string | null
- tenant_name: string (required)
- last_login: string | null
- days_inactive: integer | null

---

## CollectionStatsResponse

Collection statistics response.

**Fields:**
- collection_id: string | null
- xai_collection_id: string | null
- name: string
- document_count: integer
- total_bytes: integer
- documents_ready: integer
- documents_processing: integer
- documents_failed: integer

---

## ContactDetail

Full contact detail with call history.

**Fields:**
- id: string (required)
- first_name: string | null
- last_name: string | null
- phone: string | null
- email: string | null
- company: string | null
- tags: array of string
- calls: array of CallHistorySummary
- total_calls: integer
- stats: ContactStats | null

---

## ContactDetailResponse

Single contact with full call history.

**Fields:**
- contact: ContactDetail (required)

---

## ContactIntelligencePromptRequest

Request to update prompt with Contact Intelligence instructions.

**Fields:**
- current_prompt: string (required) — The existing system prompt to modify
- action: string (required) — Action to perform: 'add' to inject CI section, 'remove' to strip it

---

## ContactListItem

Contact in the list view.

**Fields:**
- id: string (required)
- first_name: string | null
- last_name: string | null
- phone: string | null
- email: string | null
- company: string | null
- tags: array of string
- total_calls: integer
- last_call_at: string | null

---

## ContactListResponse

Paginated contact list response.

**Fields:**
- contacts: array of ContactListItem (required)
- total: integer (required)
- next_cursor: string | null
- next_cursor_timestamp: integer | null
- has_more: boolean

---

## ContactPatchRequest

Request to update a GHL contact.

**Fields:**
- add_tags: array of string
- remove_tags: array of string
- custom_fields: array of object | null
- opportunity_id: string | null
- pipeline_stage_id: string | null

---

## ContactPatchResponse

Result of a contact patch operation.

**Fields:**
- success: boolean (required)
- tags_added: array of string
- tags_removed: array of string
- fields_updated: boolean
- stage_updated: boolean

---

## ContactStats

Aggregate stats for a contact's call history.

**Fields:**
- total_calls: integer
- avg_duration_seconds: number | null
- appointments_booked: integer
- last_call_at: string | null

---

## ConversationEvent

A single event in the conversation timeline (call or SMS).

**Fields:**
- id: string (required)
- event_type: string (required)
- direction: string (required)
- occurred_at: string (required)
- duration_seconds: integer | null
- status: string | null
- summary: string | null
- agent_name: string | null
- content: string | null
- channel: string | null

---

## ConversationTimelineResponse

Merged call + SMS timeline for a contact.

**Fields:**
- contact_phone: string (required)
- events: array of ConversationEvent (required)
- total: integer (required)
- sms_included: boolean (required)

---

## CopyAgentToSubAccountRequest

Request body for copying an agent between sub-accounts.

**Fields:**
- source_tenant_id: string (required)
- target_tenant_id: string (required)

---

## CopyFunctionRequest

Request to copy a function to another sub-account (agency feature).

**Fields:**
- target_tenant_id: string (required) — Target sub-account to copy function to

---

## CostByDirection

Cost breakdown by call direction/type.

**Fields:**
- direction: string (required)
- calls: integer (required)
- minutes: integer (required)
- cost_cents: integer (required)
- revenue_cents: integer (required)
- margin_cents: integer (required)

---

## CostByProvider

Cost breakdown by voice provider.

**Fields:**
- provider: string (required)
- provider_label: string (required)
- calls: integer (required)
- minutes: integer (required)
- cost_cents: integer (required)
- revenue_cents: integer (required)
- margin_cents: integer (required)

---

## CreateShareLinkRequest

Request to create a shareable link.

**Fields:**
- custom_slug: string | null
- expires_in_days: integer | null

---

## CreateShareLinkResponse

Response after creating a share link.

**Fields:**
- id: string (required)
- slug: string (required)
- share_url: string (required)
- is_active: boolean (required)
- expires_at: string | null

---

## CreateSubAccountRequest

Request to create a new sub-account.

**Fields:**
- name: string (required)
- slug: string (required)
- admin_email: string | null
- admin_name: string | null
- per_minute_rate_cents: integer
- monthly_platform_fee_cents: integer
- billing_start_day: integer
- upcharge_by_provider: object | null
- test_demo_upcharge_by_provider: object | null
- text_upcharge_by_type: object | null

---

## CreateUserRequest

Request to create a new user account.

**Fields:**
- email: string (required)
- password: string (required)
- plan: string enum ['starter', 'pro', 'agency']
- company_name: string | null

---

## CreateUserResponse

Response after creating a user.

**Fields:**
- id: string (required)
- email: string (required)
- tenant_id: string (required)
- tenant_name: string (required)
- plan: string (required)
- created_at: string (required)

---

## CustomFunctionCreate

Request body for creating a custom function.

**Fields:**
- name: string (required) — Function name in snake_case (e.g., check_inventory)
- description: string (required) — Description of what the function does (shown to AI)
- parameters: object — JSON Schema for function parameters
- webhook_url: string (required) — Webhook URL to call (must start with http:// or https://)
- webhook_method: string — HTTP method for webhook call
- webhook_headers: object — Custom headers to include in webhook request
- webhook_timeout_ms: integer — Timeout for webhook call in milliseconds (1000-30000)
- is_enabled: boolean — Whether the function is enabled
- speak_during_execution: boolean — Whether AI should speak while waiting for webhook response

---

## CustomFunctionResponse

Response schema for custom function data.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- agent_id: string | null
- name: string (required)
- description: string (required)
- parameters: object (required)
- webhook_url: string (required)
- webhook_method: string (required)
- webhook_headers: object (required)
- webhook_timeout_ms: integer (required)
- is_enabled: boolean (required)
- speak_during_execution: boolean (required)
- created_at: string (required)
- updated_at: string (required)

---

## CustomFunctionUpdate

Request body for updating a custom function. All fields optional.

**Fields:**
- name: string | null — Function name in snake_case
- description: string | null — Description of what the function does
- parameters: object | null — JSON Schema for function parameters
- webhook_url: string | null — Webhook URL to call
- webhook_method: string | null — HTTP method for webhook call
- webhook_headers: object | null — Custom headers to include in webhook request
- webhook_timeout_ms: integer | null — Timeout for webhook call in milliseconds
- is_enabled: boolean | null — Whether the function is enabled
- speak_during_execution: boolean | null — Whether AI should speak while waiting for webhook response

---

## DailyAgencyTrend

Daily aggregated stats for trend chart.

**Fields:**
- date: string (required)
- calls: integer (required)
- minutes: number (required)
- revenue_cents: integer (required)
- cost_cents: integer (required)
- margin_cents: integer (required)

---

## DailyTrend

One row per day in the selected range.

**Fields:**
- date: string (required)
- calls: integer
- minutes: number
- cost_cents: integer
- booked: integer

---

## DashboardStats

Schema for dashboard statistics response.

**Fields:**
- total_calls: integer (required)
- total_minutes: number (required)
- active_agents: integer (required)
- conversion_rate: number (required)
- recent_calls: array of RecentCall (required)
- usage_trend: object (required)

---

## DeletionRequestPayload

**Fields:**
- reason: string | null

---

## DemoChatMessage

A single message in a demo chat conversation.

**Fields:**
- role: string (required)
- content: string (required)

---

## DemoChatRequest

Request to send a message in a demo text chat.

**Fields:**
- messages: array of DemoChatMessage (required)
- dynamic_variables: object | null

---

## DemoChatResponse

Response from the demo text chat endpoint.

**Fields:**
- messages: array of string (required)
- greeting: string | null

---

## DemoConfigCreate

Request to create a demo config.

**Fields:**
- agent_id: string (required)
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] (required)
- name: string (required)
- config: object
- after_cta_text: string | null
- after_cta_url: string | null
- webhook_url: string | null
- expires_in_days: integer | null

---

## DemoConfigListItem

Summary for the demo management grid.

**Fields:**
- id: string (required)
- name: string (required)
- channel: string (required)
- agent_name: string
- slug: string (required)
- config: object
- view_count: integer
- call_count: integer
- created_at: string (required)
- expires_at: string | null

---

## DemoConfigResponse

Full demo config response.

**Fields:**
- id: string (required)
- agent_id: string (required)
- tenant_id: string (required)
- slug: string (required)
- name: string (required)
- channel: string (required)
- config: object
- is_active: boolean
- view_count: integer
- call_count: integer
- demo_url: string
- after_cta_text: string | null
- after_cta_url: string | null
- webhook_url: string | null
- created_at: string (required)
- updated_at: string (required)
- expires_at: string | null

---

## DemoConfigUpdate

Request to update a demo config (all optional).

**Fields:**
- name: string | null
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] | null
- config: object | null
- is_active: boolean | null
- after_cta_text: string | null
- after_cta_url: string | null
- webhook_url: string | null
- expires_in_days: integer | null

---

## DemoEventCreate

Request to track a demo event.

**Fields:**
- event_type: string (required)
- duration_s: integer | null
- metadata: object

---

## DirectionBreakdown

Call count grouped by direction.

**Fields:**
- direction: string (required)
- count: integer

---

## DocumentListResponse

List of documents response.

**Fields:**
- documents: array of DocumentResponse (required)
- total: integer (required)

---

## DocumentResponse

Document data response.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- collection_id: string (required)
- xai_document_id: string | null
- filename: string (required)
- content_type: string (required)
- file_size: integer (required)
- status: string (required)
- error_message: string | null
- description: string | null
- source_type: string | null
- created_at: string (required)
- updated_at: string (required)

---

## EmbedSSORequest

Request body for embedded SSO endpoint.

**Fields:**
- payload: string (required) — Encrypted SSO payload from partner platform

---

## EmotionTagItem

An emotion tag with name and description.

**Fields:**
- name: string (required)
- description: string (required)

---

## EnabledChannels

Per-channel AI enable/disable settings.

Supports both legacy boolean format and new ChannelConfig format:
- Legacy: {"sms": true, "instagram": false}
- New: {"sms": {"enabled": true, "accounts": []}, "instagram": {"enabled": true, "accounts": ["@mybusiness"]}}

**Fields:**
- sms: boolean | ChannelConfig
- whatsapp: boolean | ChannelConfig
- instagram: boolean | ChannelConfig
- facebook: boolean | ChannelConfig
- tiktok: boolean | ChannelConfig
- live_chat: boolean | ChannelConfig

---

## EnhanceDescriptionRequest

Request to enhance a business description.

**Fields:**
- business_name: string (required)
- industry: string (required)
- description: string (required)

---

## EnhanceDescriptionResponse

Response with enhanced description.

**Fields:**
- enhanced_description: string (required)

---

## EnrichedContactDetail

Extended contact detail with GHL pipeline + custom field enrichment.

**Fields:**
- id: string (required)
- first_name: string | null
- last_name: string | null
- phone: string | null
- email: string | null
- company: string | null
- tags: array of string
- calls: array of CallHistorySummary
- total_calls: integer
- stats: ContactStats | null
- pipeline_stage: string | null
- pipeline_name: string | null
- deal_value: number | null
- custom_fields: object
- upcoming_appointments: array of AppointmentEntry
- past_appointments: array of AppointmentEntry

---

## EnrichedContactDetailResponse

Single contact with enriched GHL data.

**Fields:**
- contact: EnrichedContactDetail (required)

---

## EnrollmentCreate

**Fields:**
- contact_phone: string (required) — E.164 format
- contact_name: string | null
- contact_email: string | null
- contact_id: string | null
- timezone: string

---

## EnrollmentListResponse

**Fields:**
- enrollments: array of EnrollmentResponse (required)
- total: integer (required)

---

## EnrollmentResponse

**Fields:**
- id: string (required)
- tenant_id: string (required)
- sequence_id: string (required)
- contact_id: string | null
- contact_phone: string (required)
- contact_name: string | null
- contact_email: string | null
- current_step: integer (required)
- status: string (required)
- next_action_at: string | null
- timezone: string (required)
- total_calls: integer (required)
- total_texts: integer (required)
- total_attempts: integer (required)
- last_call_outcome: string | null
- enrolled_via: string (required)
- enrolled_at: string (required)
- completed_at: string | null
- created_at: string (required)
- updated_at: string (required)

---

## FAQPairCreate

A single FAQ pair for creation.

**Fields:**
- question: string (required)
- answer: string (required)

---

## FAQPairResponse

FAQ pair response.

**Fields:**
- id: string (required)
- source_id: string (required)
- question: string (required)
- answer: string (required)
- sort_order: integer
- created_at: string (required)
- updated_at: string (required)

---

## FAQPairUpdate

Update a single FAQ pair.

**Fields:**
- question: string | null
- answer: string | null
- sort_order: integer | null

---

## FAQSourceCreate

Request body for creating an FAQ source.

**Fields:**
- name: string (required)
- pairs: array of FAQPairCreate

---

## FAQSourceResponse

FAQ source response with pairs.

**Fields:**
- id: string (required)
- collection_id: string (required)
- name: string (required)
- source_type: string
- pairs: array of FAQPairResponse
- document_id: string | null
- created_at: string (required)
- updated_at: string (required)

---

## FollowUpActivityResponse

**Fields:**
- jobs: array of FollowUpJobResponse (required)
- total: integer (required)
- pending_count: integer (required)
- completed_count: integer (required)
- stopped_count: integer (required)
- failed_count: integer (required)

---

## FollowUpJobResponse

**Fields:**
- id: string (required)
- tenant_id: string (required)
- text_conversation_id: string (required)
- text_assistant_id: string (required)
- ghl_conversation_id: string | null
- ghl_contact_id: string | null
- ghl_location_id: string | null
- provider: string
- phone_number_id: string | null
- scenario: string (required)
- step_number: integer (required)
- channel: string (required)
- fallback_channel: string | null (required)
- scheduled_for: string (required)
- status: string (required)
- stop_reason: string | null (required)
- generated_message: string | null (required)
- message_context: string | null (required)
- webhook_url: string | null (required)
- attempts: integer (required)
- last_error: string | null (required)
- executed_at: string | null (required)
- created_at: string (required)
- updated_at: string (required)

---

## ForgotPasswordRequest

Request body for forgot password (sends reset email).

**Fields:**
- email: string (required)

---

## FunctionCallEntry

A single function call executed during an AI message.

**Fields:**
- function: string (required)
- arguments: object | null
- result: object | null
- success: boolean | null
- timestamp: string | null

---

## FunctionCallLog

A single function call log entry.

**Fields:**
- function: string (required) — Function name that was called
- arguments: object (required) — Arguments passed to the function
- result: ? (required) — Result returned from the function
- success: boolean (required) — Whether the function call succeeded
- timestamp: string (required) — ISO timestamp of when the call was made

---

## FunctionForUpdate

A custom function to integrate into the prompt.

**Fields:**
- name: string (required)
- description: string (required)
- parameters: object

---

## FunctionLibraryResponse

Response schema for the functions library (tenant-level).

**Fields:**
- functions: array of FunctionWithAgentsResponse (required)
- total: integer (required)

---

## FunctionSuggestion

A single tool suggestion with reason.

**Fields:**
- tool_name: string (required)
- reason: string (required)

---

## FunctionTestRequest

Request body for testing a custom function's webhook.

**Fields:**
- arguments: object — Arguments to pass to the function
- contact_id: string — GHL contact ID — always present via Contact Intelligence

---

## FunctionTestResponse

Response schema for function test result.

**Fields:**
- success: boolean (required)
- status_code: integer | null
- response_time_ms: number (required)
- response_body: ? | null
- error: string | null
- signature: string | null — HMAC signature that was sent (for verification)

---

## FunctionWithAgentsResponse

Response schema for a function with its attached agents.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- name: string (required)
- description: string (required)
- parameters: object (required)
- webhook_url: string (required)
- webhook_method: string (required)
- webhook_headers: object (required)
- webhook_timeout_ms: integer (required)
- speak_during_execution: boolean (required)
- created_at: string (required)
- updated_at: string (required)
- agent_count: integer
- agents: array of object

---

## GHLApiKeyRequest

Request schema for connecting GHL with a Private Integration API key.

**Fields:**
- api_key: string (required) — GHL Private Integration API key
- location_id: string (required) — GHL Location ID

---

## GHLIntegrationInfo

Information about a GoHighLevel integration for multi-account selection.

**Fields:**
- id: string (required)
- location_id: string (required)
- location_name: string (required)

---

## GenerateAllKnowledgeResponse

Response with all generated knowledge sections.

**Fields:**
- services: string (required)
- pricing: string (required)
- team: string (required)
- faqs: string (required)

---

## GenerateExpressiveRequest

Request to generate expressive voice configuration.

**Fields:**
- current_prompt: string (required) — The existing system prompt for context
- preset: string | null — Preset style: empathetic_support, high_energy_sales, professional_service, friendly_fun
- custom_description: string | null — Free-text description of desired emotional delivery
- refinement: string | null — Refinement instruction for a previous result
- previous_result: object | null — Previous AI output to refine

---

## GenerateExpressiveResponse

Response with generated expressive voice configuration.

**Fields:**
- audio_tags: array of string (required)
- emotion_tags: array of EmotionTagItem (required)
- prompt_section: string (required)
- changes_summary: string (required)
- updated_prompt: string (required)

---

## GenerateFAQRequest

Request body for AI-generating FAQ pairs from content.

**Fields:**
- content: string (required) — Content to extract FAQs from
- num_pairs: integer

---

## GenerateFunctionSchemaRequest

Request to generate a custom function schema using AI.

**Fields:**
- description: string (required) — Plain English description of what the function should do
- webhook_purpose: string | null — Optional context about where the webhook sends data

---

## GenerateFunctionSchemaResponse

Response with AI-generated function schema.

**Fields:**
- name: string (required)
- description: string (required)
- parameters: object (required)
- webhook_method: string (required)

---

## GenerateKnowledgeResponse

Response with generated knowledge section.

**Fields:**
- section: string (required)
- suggestion: string (required)

---

## GenerateScenarioRequest

Generate a simulation scenario from a natural language description.

**Fields:**
- description: string (required) — Natural language scenario description
- model: string

---

## HTTPValidationError

**Fields:**
- detail: array of ValidationError

---

## HealthBreakdown

Breakdown of health score components.

**Fields:**
- login_recency: number
- usage_volume: number
- active_agents: number
- call_volume: number
- no_issues: number

---

## HealthScore

Health score with status and breakdown.

**Fields:**
- score: integer (required)
- status: string enum ['healthy', 'warning', 'at_risk'] (required)
- breakdown: HealthBreakdown (required)

---

## ImportFromUrlRequest

Request to import demo config from a website URL.

**Fields:**
- url: string (required) — Website URL to analyze (e.g., https://example.com)
- channel: string enum ['phone', 'sms', 'web', 'orb', 'fb_messenger', 'ig_messenger' (+4 more)] (required) — Demo channel type

---

## ImportGHLNumbersRequest

Request to import GoHighLevel phone numbers.

**Fields:**
- phone_numbers: array of object (required) — List of GHL phone numbers to import

---

## ImportNumbersRequest

Request to import one or more phone numbers.

**Fields:**
- phone_number_sids: array of string (required) — List of Twilio phone number SIDs to import
- configure_sip: boolean — DEPRECATED - No longer used (kept for API compatibility)

---

## ImportWebsiteRequest

Request to import business info from a website.

**Fields:**
- url: string (required) — Website URL to scrape (e.g., https://example.com)

---

## ImportWebsiteResponse

Response with extracted business information.

**Fields:**
- business_name: string | null
- industry: string | null
- description: string | null
- services: string | null
- pricing: string | null
- team: string | null
- faqs: string | null
- urls_scraped: array of string
- partial_success: boolean
- warnings: array of string

---

## IndustryPresetsResponse

Response with available industry presets.

**Fields:**
- industries: array of string (required)
- presets: object (required)

---

## IntegrationInfo

Integration info for assignment.

**Fields:**
- id: string (required)
- provider: string (required)
- provider_account_id: string | null
- account_name: string | null
- location_name: string | null
- is_active: boolean (required)
- created_at: string (required)

---

## IntegrationStatus

Status of an integration.

**Fields:**
- id: string (required)
- provider: string (required)
- is_connected: boolean (required)
- is_active: boolean (required)
- account_name: string | null
- account_id: string | null
- expires_at: string | null
- calendars: array of CalendarInfo

---

## InvoiceItem

Stripe invoice item.

**Fields:**
- id: string (required)
- amount_due: integer (required)
- amount_paid: integer (required)
- status: string (required)
- period_start: string (required)
- period_end: string (required)
- invoice_pdf: string | null

---

## InvoiceListResponse

Response containing list of invoices.

**Fields:**
- invoices: array of InvoiceItem (required)

---

## InvoiceSubAccountLine

Per-sub-account billing line item for invoice summary.

**Fields:**
- id: string (required)
- name: string (required)
- voice_minutes: number (required)
- voice_calls: integer (required)
- voice_revenue_cents: integer (required)
- text_count: integer (required)
- text_revenue_cents: integer (required)
- platform_fee_cents: integer (required)
- total_due_cents: integer (required)

---

## InvoiceSummaryResponse

Aggregated invoice summary across all sub-accounts for current billing period.

**Fields:**
- period_start: string (required)
- period_end: string (required)
- sub_accounts: array of InvoiceSubAccountLine (required)
- grand_total_cents: integer (required)
- grand_voice_revenue_cents: integer (required)
- grand_text_revenue_cents: integer (required)
- grand_platform_fees_cents: integer (required)

---

## IssueReportResponse

Issue report response.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- user_id: string | null
- user_email: string | null
- tenant_name: string | null
- message: string (required)
- url: string | null
- page_name: string | null
- browser_info: string | null
- image_url: string | null
- created_at: string (required)
- resolved: boolean (required)
- resolved_at: string | null

---

## IssueResolveRequest

Request to resolve/unresolve an issue.

**Fields:**
- resolved: boolean (required)

---

## KnowledgeBaseCreate

Request body for creating a Knowledge Base.

**Fields:**
- name: string (required) — Name of the Knowledge Base

---

## KnowledgeBaseListResponse

List of Knowledge Bases response.

**Fields:**
- knowledge_bases: array of KnowledgeBaseResponse (required)
- total: integer (required)

---

## KnowledgeBaseResponse

Knowledge Base data response.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- xai_collection_id: string (required)
- name: string (required)
- document_count: integer
- total_bytes: integer
- created_at: string (required)
- updated_at: string (required)

---

## KnowledgeBaseUpdate

Request body for updating a Knowledge Base.

**Fields:**
- name: string (required) — New name for the Knowledge Base

---

## LinkedAgentSummary

Summary of linked agent for display.

**Fields:**
- id: string (required)
- name: string (required)
- tools_enabled: array of string

---

## LinkedTextAssistantSummary

Minimal text assistant info returned with agent responses.

**Fields:**
- id: string (required)
- is_active: boolean (required)
- enabled_channels: object | null

---

## LoginRequest

Request body for user login.

**Fields:**
- email: string (required)
- password: string (required)

---

## LogoUploadResponse

Response after uploading logo.

**Fields:**
- logo_url: string (required)
- file_size: integer (required)

---

## MCPServerConfig

Per-agent MCP server. Used for create/update payloads.

Bearer token semantics for PATCH (mirrored exactly in
`_upsert_mcp_servers_for_agent`):
  - field absent / None  -> preserve existing ciphertext
  - empty string ""      -> explicit clear (revoke stored bearer)
  - non-empty plaintext  -> replace (encrypt new value)

**Fields:**
- server_url: string (required)
- server_label: string (required)
- server_description: string | null
- bearer_token: string | null
- allowed_tools: array of string | null
- enabled: boolean

---

## MCPServerSummary

Read model: never includes ciphertext or plaintext bearer.

**Fields:**
- id: string (required)
- server_url: string (required)
- server_label: string (required)
- server_description: string | null
- auth_configured: boolean (required)
- allowed_tools: array of string | null
- enabled: boolean (required)

---

## MSImportRequest

Body for POST /sms-pools/ — import an existing Twilio MS as a pool.

**Fields:**
- messaging_service_sid: string (required)
- integration_id: string (required)
- name: string | null

---

## MSListItem

A Twilio Messaging Service visible to a tenant (across all their integrations).

**Fields:**
- sid: string (required)
- friendly_name: string (required)
- sticky_sender: boolean | null
- area_code_geomatch: boolean | null
- scaler: boolean | null
- inbound_request_url: string | null
- integration_id: string (required)

---

## MeResponse

Response for /auth/me endpoint.

**Fields:**
- user: UserResponse (required)
- tenant: TenantResponse (required)

---

## MostActiveUser

Most active user for leaderboard.

**Fields:**
- id: string (required)
- email: string (required)
- full_name: string | null
- logins_30d: integer (required)

---

## NoteCreateRequest

Request to create a note on a GHL contact.

**Fields:**
- body: string (required)

---

## NoteResponse

A single note from GHL.

**Fields:**
- id: string (required)
- body: string (required)
- created_at: string | null
- created_by: string | null

---

## NotesListResponse

List of notes for a contact.

**Fields:**
- notes: array of NoteResponse (required)
- total: integer (required)

---

## NotificationListResponse

Paginated list of notifications.

**Fields:**
- notifications: array of NotificationResponse (required)
- total: integer (required)
- unread_count: integer (required)

---

## NotificationResponse

Single in-app notification.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- type: string (required)
- title: string (required)
- body: string (required)
- metadata: object
- is_read: boolean (required)
- created_at: string (required)
- source_account_name: string | null

---

## NotificationSettingsResponse

Notification settings response with metadata.

**Fields:**
- email_new_call: boolean
- email_call_summary: boolean
- email_low_balance: boolean
- email_weekly_digest: boolean
- additional_emails: array of string
- quiet_hours_enabled: boolean
- quiet_hours_start: string
- quiet_hours_end: string
- quiet_hours_timezone: string
- notification_frequency: string enum ['immediate', 'daily', 'weekly']
- sms_enabled: boolean
- id: string (required)
- tenant_id: string (required)
- created_at: string (required)
- updated_at: string (required)

---

## NotificationSettingsUpdate

Request body for updating notification settings.

**Fields:**
- email_new_call: boolean | null
- email_call_summary: boolean | null
- email_low_balance: boolean | null
- email_weekly_digest: boolean | null
- additional_emails: array of string | null
- quiet_hours_enabled: boolean | null
- quiet_hours_start: string | null
- quiet_hours_end: string | null
- quiet_hours_timezone: string | null
- notification_frequency: string enum ['immediate', 'daily', 'weekly'] | null
- sms_enabled: boolean | null

---

## OnboardingProgress

Onboarding progress response model.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- current_step: integer
- completed_steps: array of integer
- account_type: string | null
- business_name: string | null
- industry: string | null
- ghl_connected: boolean
- ghl_integration_id: string | null
- phone_number_id: string | null
- sub_account_id: string | null
- agent_id: string | null
- deployed: boolean
- calendar_connected: boolean
- phone_purchased: boolean
- agent_created: boolean
- test_call_completed: boolean
- completed_at: string | null
- created_at: string (required)
- updated_at: string (required)

---

## OperatingHours

Business hours constraint for when the sequence can execute steps.

**Fields:**
- start: string — Start time in HH:MM 24h format
- end: string — End time in HH:MM 24h format
- days: array of integer — ISO weekdays (1=Mon..7=Sun)
- timezone: string — IANA timezone for the operating hours

---

## OutboundCallRequest

Request to initiate an outbound call.

**Fields:**
- to_number: string (required) — Recipient phone number in E.164 format (e.g., +14155551234)
- from_phone_number_id: string | null — Specific phone number to call from. If not provided, uses agent's primary number.
- ghl_contact_id: string | null — GHL contact ID for pre-flight conversation checks

---

## OutboundCallResponse

Response after initiating an outbound call.

**Fields:**
- call_id: string (required) — Internal call log ID
- call_sid: string (required) — Twilio call SID
- status: string (required) — Initial call status
- from_number: string (required) — Calling from number
- to_number: string (required) — Calling to number
- agent_id: string (required) — Agent handling the call
- initiated_at: string (required) — When call was initiated

---

## OutboundComplianceStatus

Response: current outbound compliance status for a tenant.

**Fields:**
- outbound_enabled: boolean (required)
- terms_version: string | null
- accepted_at: string | null
- accepted_by: string | null

---

## OutboundTextSendRequest

Request body for sending an outbound text message.

**Fields:**
- phone_number: string | null
- ghl_contact_id: string | null
- message: string | null
- ai_generate: boolean
- ai_context: string | null
- channel: string

---

## OutboundTextSendResponse

Response for outbound text send.

**Fields:**
- success: boolean (required)
- messages_sent: integer (required)
- messages: array of string (required)
- conversation_id: string | null
- contact_id: string | null
- channel: string (required)

---

## PaginatedUsersResponse

Paginated list of users with analytics.

**Fields:**
- items: array of UserListItem (required)
- total: integer (required)
- page: integer (required)
- per_page: integer (required)
- has_more: boolean (required)

---

## PendingSignupRequest

Request body for Payment-First signup (account created after payment).

**Fields:**
- email: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)
- company_name: string (required)
- plan: string enum ['payg', 'starter', 'agency', 'pro']
- billing_period: string enum ['monthly', 'annual']
- tos_accepted: boolean — User must accept Terms of Service and Privacy Policy
- affiliate_code: string | null
- utm_source: string | null
- utm_medium: string | null
- utm_campaign: string | null
- utm_content: string | null
- utm_term: string | null
- referrer_url: string | null

---

## PendingSignupResponse

Response with Stripe checkout URL for Payment-First signup.

**Fields:**
- checkout_url: string (required)

---

## PhoneNumberListResponse

Response schema for listing phone numbers.

**Fields:**
- phone_numbers: array of PhoneNumberResponse (required)
- total: integer (required)

---

## PhoneNumberPurchase

Request schema for purchasing a phone number.

**Fields:**
- phone_number: string (required) — E.164 format: +14155551234

---

## PhoneNumberResponse

Response schema for a phone number.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- twilio_sid: string (required)
- phone_number: string (required)
- friendly_name: string | null
- agent_id: string | null
- is_active: boolean
- monthly_cost_cents: integer (required)
- created_at: string (required)
- sub_account_name: string | null
- sub_account_id: string | null
- voice_capable: boolean
- sms_capable: boolean
- mms_capable: boolean
- source: string
- a2p_campaign_id: string | null
- a2p_status: string
- a2p_verified_at: string | null
- a2p_last_checked: string | null
- messaging_enabled: boolean
- a2p_metadata: object | null

---

## PhoneNumberSummary

Phone number summary for user detail.

**Fields:**
- id: string (required)
- phone_number: string (required)
- friendly_name: string | null
- created_at: string (required)

---

## PhoneNumberUpdate

Request schema for updating a phone number.

**Fields:**
- agent_id: string | null — Assign to agent
- friendly_name: string | null — Display name

---

## PlanDistributionItem

Plan distribution for donut chart.

**Fields:**
- label: string (required)
- value: integer (required)

---

## PoolMemberResponse

A phone number attached to a pool, with today's usage stats.

**Fields:**
- id: string (required)
- phone_number_id: string (required)
- phone_number: string (required)
- first_used_date: string | null
- status: string enum ['active', 'quarantined', 'paused', 'removed'] (required)
- quarantined_until: string | null
- quarantine_reason: string | null
- last_used_at: string | null
- today_sent: integer
- today_cap: integer

---

## PoolResponse

A pool row with its members expanded.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- sub_account_id: string | null
- integration_id: string (required)
- name: string (required)
- messaging_service_sid: string (required)
- warm_up_days: integer (required)
- daily_cap_max: integer (required)
- daily_cap_start: integer (required)
- status: string (required)
- created_at: string (required)
- members: array of PoolMemberResponse
- import_warnings: array of string

---

## PortalRequest

Request to create a Stripe Customer Portal session.

**Fields:**
- return_url: string | null

---

## PortalResponse

Response containing Stripe Portal URL.

**Fields:**
- portal_url: string (required)

---

## PreviewGreetingTTSRequest

Request to preview a greeting via TTS.

**Fields:**
- text: string (required)
- voice_provider: string (required)
- voice_id: string (required)

---

## PreviewPromptRequest

Request to preview the full generated prompt.

**Fields:**
- business_name: string (required)
- agent_name: string
- industry: string
- personality: string
- description: string
- services: string
- pricing: string
- team: string
- faqs: string
- product_offer: string
- qualification_criteria: string
- common_objections: string
- voice_provider: string
- agent_type: string | null
- sales_methodology: string | null
- cta_type: string | null

---

## PreviewPromptResponse

Response with the full generated prompt and recommended settings.

**Fields:**
- system_prompt: string (required)
- greeting: string (required)
- recommended_settings: object (required)

---

## ProviderBreakdown

Usage breakdown by voice provider.

**Fields:**
- provider: string (required)
- provider_label: string (required)
- calls: integer (required)
- minutes: number (required)
- cost_cents: integer (required)
- revenue_cents: integer (required)
- margin_cents: integer (required)

---

## ProviderUsage

Usage breakdown for a single voice provider.

**Fields:**
- provider: string (required)
- provider_label: string (required)
- calls: integer (required)
- minutes: number (required)
- rate_cents: integer (required)
- cost_cents: integer (required)

---

## PublicAgentResponse

Public-facing agent info for the demo page (no sensitive data).

**Fields:**
- agent_name: string (required)
- business_name: string | null
- industry: string | null
- greeting: string | null
- voice: string | null
- voice_provider: string | null

---

## PublicBrandingResponse

**Fields:**
- company_name: string (required)
- logo_url: string | null
- favicon_url: string | null
- primary_color: string

---

## PublicCheckoutRequest

Request for unauthenticated checkout (Stripe-first signup).

**Fields:**
- email: string (required)
- plan: string enum ['payg', 'starter', 'agency', 'pro'] (required)
- billing_period: string enum ['monthly', 'annual']
- affiliate_code: string | null

---

## PublicDemoResponse

Public-facing demo config for the demo page (no sensitive data).

**Fields:**
- channel: string (required)
- config: object
- name: string
- agent_name: string (required)
- business_name: string | null
- industry: string | null
- greeting: string | null
- voice: string | null
- voice_provider: string | null
- after_cta_text: string | null
- after_cta_url: string | null
- branding: object | null
- expires_at: string | null
- variable_definitions: array of object | null

---

## RecentCall

Schema for a recent call in the dashboard.

**Fields:**
- id: string (required)
- from_number: string (required)
- duration_seconds: integer | null
- status: string (required)
- started_at: string (required)
- agent_id: string (required)
- appointment_booked: boolean (required)

---

## RefreshTokenRequest

Request body for token refresh.

**Fields:**
- refresh_token: string (required)

---

## RemoveIntegrationResponse

Response after removing an integration from sub-account.

**Fields:**
- success: boolean (required)
- sub_account_id: string (required)
- integration_id: string (required)

---

## ResetPasswordRequest

Request body for resetting password with token.

**Fields:**
- token: string (required) — Password reset token from email link
- new_password: string (required) — New password (minimum 6 characters)

---

## ResourceUsage

Usage for a single resource type.

**Fields:**
- current: integer (required)
- limit: integer (required)
- remaining: integer (required)
- unlimited: boolean (required)

---

## RewritePromptRequest

Holistically rewrite the agent's prompt incorporating all suggestions.

**Fields:**
- suggestions: array of object (required) — List of suggestion objects from suggest-prompt
- model: string

---

## RichTextCreate

Request body for creating a rich text source.

**Fields:**
- name: string (required)
- content: string (required) — Rich text / markdown content

---

## RichTextResponse

Rich text source response.

**Fields:**
- id: string (required)
- collection_id: string (required)
- name: string (required)
- source_type: string
- content: string
- document_id: string | null
- created_at: string (required)
- updated_at: string (required)

---

## RichTextUpdate

Update a rich text source.

**Fields:**
- name: string | null
- content: string | null

---

## SaveRewrittenPromptRequest

Save an approved rewritten prompt to the agent.

**Fields:**
- rewritten_prompt: string (required)

---

## ScenarioCriterion

**Fields:**
- name: string (required) — Criterion name, e.g. 'Appointment Booked'
- description: string (required) — What the judge evaluates

---

## ScenarioRequest

Run a simulation with a named scenario or custom config.

**Fields:**
- scenario_name: string | null
- persona: string | null
- description: string | null
- criteria: array of ScenarioCriterion
- judge_model: string
- simulator_model: string
- max_turns: integer

---

## ScheduledCallCreate

Schema for creating a scheduled call.

**Fields:**
- agent_id: string (required)
- to_phone_number: string (required) — Recipient phone number in E.164 format
- scheduled_for: string (required) — When to call (ISO 8601 format, will be stored as UTC)
- timezone: string — User's timezone for display purposes
- contact_id: string | null — GHL contact ID if known
- contact_name: string | null — Contact name for display
- phone_number_id: string | null — Specific phone number to call from (uses agent default if not provided)
- is_callback: boolean — True if this is a return call
- previous_call_log_id: string | null — ID of the call that requested this callback
- callback_context: string | null — Summary of previous conversation for context-aware greeting

---

## ScheduledCallListResponse

Response schema for listing scheduled calls.

**Fields:**
- scheduled_calls: array of ScheduledCallResponse (required)
- total: integer (required)

---

## ScheduledCallResponse

Response schema for a scheduled call.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- agent_id: string | null
- agent_name: string | null
- phone_number_id: string | null
- from_phone_number: string | null
- contact_id: string | null
- contact_name: string | null
- to_phone_number: string (required)
- scheduled_for: string (required)
- timezone: string (required)
- status: string (required)
- is_callback: boolean
- previous_call_log_id: string | null
- callback_context: string | null
- call_log_id: string | null
- attempts: integer
- last_error: string | null
- dialed_at: string | null
- source: string
- confidence: number
- created_by: string | null
- created_at: string (required)
- updated_at: string (required)

---

## ScheduledCallRetry

Schema for retrying a failed scheduled call.

**Fields:**
- scheduled_for: string | null — New time to schedule. If not provided, schedules immediately.

---

## ScheduledCallUpdate

Schema for updating a scheduled call.

**Fields:**
- scheduled_for: string | null
- timezone: string | null
- status: string enum ['pending', 'cancelled'] | null
- contact_name: string | null

---

## ScrapeWebsiteRequest

Request to scrape a website and extract business info.

**Fields:**
- url: string (required) — Website URL to scrape

---

## ScrapeWebsiteResponse

Extracted business information from a website.

**Fields:**
- business_name: string | null
- industry: string | null
- description: string | null
- services: string | null
- pricing: string | null
- team: string | null
- faqs: string | null
- urls_scraped: array of string

---

## ScreenshotRequest

Request to capture a website screenshot.

**Fields:**
- url: string (required) — Website URL to screenshot
- width: integer
- height: integer
- full_page: boolean

---

## ScreenshotResponse

Screenshot capture result.

**Fields:**
- screenshot_url: string (required)
- width: integer (required)
- height: integer (required)

---

## SearchRequest

Request body for searching documents.

**Fields:**
- query: string (required)
- max_results: integer

---

## SearchResponse

Search results response.

**Fields:**
- results: array of SearchResult (required)
- query: string (required)

---

## SearchResult

A single search result.

**Fields:**
- document_id: string (required)
- filename: string (required)
- content: string (required)
- score: number (required)

---

## SequenceCreate

**Fields:**
- name: string (required)
- description: string | null
- agent_id: string (required)
- phone_number_id: string | null
- pool_id: string | null
- active_tag: string | null
- continuous_add: boolean
- steps: array of SequenceStep (required)
- max_attempts: integer
- stop_on_booking: boolean
- stop_on_reply: boolean
- operating_hours: OperatingHours | null
- template_id: string | null
- qualification_criteria: string | null

---

## SequenceListResponse

**Fields:**
- sequences: array of SequenceResponse (required)
- total: integer (required)

---

## SequenceResponse

**Fields:**
- id: string (required)
- tenant_id: string (required)
- name: string (required)
- description: string | null
- agent_id: string (required)
- phone_number_id: string | null
- pool_id: string | null
- active_tag: string | null
- continuous_add: boolean
- steps: array of object (required)
- max_attempts: integer (required)
- stop_on_booking: boolean (required)
- stop_on_reply: boolean (required)
- is_active: boolean (required)
- operating_hours: object | null
- template_id: string | null
- qualification_criteria: string | null
- created_at: string (required)
- updated_at: string (required)
- agent_name: string | null
- phone_number: string | null
- enrolled_count: integer
- active_count: integer
- booked_count: integer
- interested_count: integer
- qualified_count: integer
- not_qualified_count: integer
- booking_rate: number

---

## SequenceStats

**Fields:**
- enrolled_count: integer (required)
- active_count: integer (required)
- completed_count: integer (required)
- booked_count: integer (required)
- cancelled_count: integer (required)
- opted_out_count: integer (required)
- interested_count: integer
- qualified_count: integer
- not_qualified_count: integer
- booking_rate: number (required)

---

## SequenceStep

Single step in a sequence. Stored as JSONB array element.

**Fields:**
- type: StepType (required)
- delay_minutes: integer (required) — Minutes to wait before executing this step
- message: string | null — Message body (text and voicemail_drop steps)
- config: object — Step-specific config

---

## SequenceUpdate

**Fields:**
- name: string | null
- description: string | null
- agent_id: string | null
- phone_number_id: string | null
- pool_id: string | null
- active_tag: string | null
- continuous_add: boolean | null
- steps: array of SequenceStep | null
- max_attempts: integer | null
- stop_on_booking: boolean | null
- stop_on_reply: boolean | null
- operating_hours: OperatingHours | null
- qualification_criteria: string | null

---

## SetupStatusResponse

Aggregated setup status derived from actual tenant data.

**Fields:**
- tasks: object (required)
- completed_count: integer (required)
- total_count: integer
- required_complete: boolean (required)
- all_complete: boolean (required)

---

## ShareLinkSummary

Summary of a share link for the demo management view.

**Fields:**
- id: string (required)
- agent_id: string (required)
- agent_name: string (required)
- slug: string (required)
- share_url: string (required)
- view_count: integer
- call_count: integer
- created_at: string (required)
- expires_at: string | null

---

## SignupRequest

Request body for user signup.

**Fields:**
- email: string (required)
- password: string (required) — Minimum 6 characters (Supabase requirement)
- company_name: string (required)
- account_type: string enum ['direct', 'agency']
- tos_accepted: boolean — User must accept Terms of Service and Privacy Policy

---

## SourceListResponse

List of sources response.

**Fields:**
- sources: array of SourceResponse (required)
- total: integer (required)

---

## SourceMetrics

Metrics from a single external source.

**Fields:**
- source: string (required)
- available: boolean (required)
- data: object (required)

---

## SourceResponse

Generic source response (for list endpoints).

**Fields:**
- id: string (required)
- collection_id: string (required)
- name: string (required)
- source_type: string (required)
- document_id: string | null
- config: object
- created_at: string (required)
- updated_at: string (required)

---

## StatusBreakdown

Call count grouped by status.

**Fields:**
- status: string (required)
- count: integer

---

## StepType

**Enum:** string
Values: 'call', 'text', 'wait', 'voicemail_drop'

---

## StepUpdateRequest

Generic step update request.

**Fields:**
- account_type: string | null
- business_name: string | null
- industry: string | null
- connected: boolean | null
- purchased: boolean | null
- created: boolean | null
- completed: boolean | null
- deployed: boolean | null
- skipped: boolean | null
- agent_id: string | null
- ghl_integration_id: string | null
- phone_number_id: string | null
- sub_account_id: string | null

---

## SubAccountAgentInfo

A lightweight agent summary for the agency cross-account view.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- name: string (required)
- is_active: boolean (required)
- voice_provider: string | null
- voice: string | null
- phone_count: integer
- sub_account_name: string (required)
- created_at: string (required)

---

## SubAccountBillingResponse

Sub-account's view of their own billing info.

**Fields:**
- per_minute_rate_cents: integer (required)
- is_suspended: boolean (required)
- suspended_reason: string | null
- agency_name: string (required)
- calls_this_period: integer (required)
- minutes_this_period: number (required)
- cost_this_period_cents: integer (required)
- usage_by_provider: array of ProviderUsage
- text_messages_count: integer
- text_messages_cost_cents: integer

---

## SubAccountFunctionInfo

A custom function from a sub-account (for sharing UI).

**Fields:**
- id: string (required)
- name: string (required)
- description: string (required)
- webhook_url: string (required)
- webhook_method: string (required)
- created_at: string (required)
- sub_account_id: string (required)
- sub_account_name: string (required)

---

## SubAccountIntegrationInfo

Integration assigned to a sub-account.

**Fields:**
- id: string (required)
- provider: string (required)
- provider_account_id: string | null
- account_name: string | null
- is_active: boolean (required)
- assigned_at: string (required)

---

## SubAccountIntegrationsResponse

Sub-account's assigned integrations.

**Fields:**
- has_integrations: boolean (required)
- integrations: array of IntegrationInfo
- ghl_count: integer
- twilio_count: integer

---

## SubAccountListResponse

List of sub-accounts.

**Fields:**
- sub_accounts: array of SubAccountResponse (required)
- total_count: integer (required)

---

## SubAccountResponse

Sub-account with billing and stats.

**Fields:**
- id: string (required)
- name: string (required)
- slug: string (required)
- admin_email: string | null
- admin_name: string | null
- is_active: boolean (required)
- created_at: string (required)
- per_minute_rate_cents: integer (required)
- monthly_platform_fee_cents: integer (required)
- is_suspended: boolean (required)
- suspended_reason: string | null
- billing_start_day: integer
- upcharge_by_provider: object | null
- test_demo_upcharge_by_provider: object | null
- text_upcharge_by_type: object | null
- integrations: array of SubAccountIntegrationInfo
- integration_id: string | null
- total_calls: integer
- total_minutes: number
- agents_count: integer
- total_texts: integer

---

## SubscriptionStatus

Current subscription status and usage.

**Fields:**
- plan: string (required)
- status: string (required)
- current_period_start: string (required)
- current_period_end: string (required)
- cancel_at_period_end: boolean (required)
- usage: UsageSummary | null

---

## SuggestFunctionsRequest

Request to get AI-powered function suggestions for an agent.

**Fields:**
- industry: string (required) — Business industry
- agent_mode: string — Agent mode: inbound, outbound, or both
- description: string — Business description for context
- has_ghl: boolean — Whether GoHighLevel CRM is connected
- system_prompt: string | null — Existing system prompt for deeper context

---

## SuggestFunctionsResponse

Response with AI-generated function suggestions.

**Fields:**
- suggestions: array of FunctionSuggestion (required)

---

## SuggestPromptRequest

Generate prompt improvements from analysis.

**Fields:**
- analysis_ids: array of string — Call analysis IDs to base suggestions on
- simulation_id: string | null
- failures: array of object — Inline failure data: [{name, reasoning, call_summary}]
- model: string

---

## TableSourceCreate

Request body for creating a table source.

**Fields:**
- name: string (required)
- headers: array of string (required)
- table_data: array of array of string

---

## TableSourceResponse

Table source response.

**Fields:**
- id: string (required)
- collection_id: string (required)
- name: string (required)
- source_type: string
- headers: array of string
- table_data: array of array of string
- document_id: string | null
- created_at: string (required)
- updated_at: string (required)

---

## TableSourceUpdate

Update a table source.

**Fields:**
- name: string | null
- headers: array of string | null
- table_data: array of array of string | null

---

## TaskStatus

Status of a single setup task.

**Fields:**
- complete: boolean (required)
- detail: string | null

---

## TenantDetailResponse

Detailed tenant response with stats.

**Fields:**
- id: string (required)
- name: string (required)
- slug: string (required)
- tenant_type: string (required)
- plan: string (required)
- agent_limit: integer (required)
- sub_account_limit: integer (required)
- is_active: boolean (required)
- trial_ends_at: string | null
- created_at: string | null
- stats: TenantStats (required)

---

## TenantResponse

Tenant data response.

**Fields:**
- id: string (required)
- name: string (required)
- slug: string (required)
- tenant_type: string (required)
- plan: string (required)
- tier: string | null
- agent_limit: integer (required)
- sub_account_limit: integer (required)
- is_active: boolean (required)
- trial_ends_at: string | null
- parent_tenant_id: string | null
- stripe_subscription_id: string | null
- subscription_status: string | null
- effective_plan: string | null
- white_label_enabled: boolean

---

## TenantStats

Tenant usage statistics.

**Fields:**
- total_agents: integer
- active_agents: integer
- total_phone_numbers: integer
- total_calls_this_month: integer
- total_minutes_this_month: number

---

## TenantUpdate

Request body for updating tenant settings.

**Fields:**
- name: string | null
- webhook_url: string | null
- webhook_enabled: boolean | null
- ghl_conversation_sync_enabled: boolean | null

---

## TestChatRequest

Request for text-based agent testing.

**Fields:**
- agent_id: string (required) — Agent ID to test
- messages: array of ChatMessage (required) — Conversation history including new user message

---

## TestChatResponse

Response from text-based agent testing.

**Fields:**
- message: ChatMessage (required) — AI assistant response
- model: string (required) — Model used (e.g., grok-2-1212)
- usage: object | null — Token usage if available
- function_calls: array of FunctionCallLog | null — Function calls made during response generation

---

## TestVoiceRequest

Request for voice-based agent testing.

**Fields:**
- agent_id: string (required) — Agent ID to test
- audio_base64: string (required) — Base64-encoded PCM16 audio at 24kHz

---

## TestVoiceResponse

Response from voice-based agent testing.

**Fields:**
- audio_base64: string (required) — Base64-encoded PCM16 audio at 24kHz from AI
- transcript: string (required) — Text transcript of AI response
- model: string (required) — Model used (e.g., grok-2-1212)

---

## TextAssistantCreate

Request body for creating a text assistant.

Text assistants now REQUIRE linking to a voice agent.
The agent provides the AI personality (prompt, temperature, greeting).

**Fields:**
- name: string (required)
- agent_id: string (required) — Link to a voice agent. Required - inherits prompt and functions from agent.
- active_tag: string | null — GHL contact tag that activates this assistant
- mode: string
- business_hours: object | null
- timezone: string
- enabled_channels: EnabledChannels | null
- human_takeover_timeout_hours: integer
- delayed_trigger_enabled: boolean
- schedule_text_back_enabled: boolean
- ghl_integration_id: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- text_model: string — AI model for text message responses

---

## TextAssistantListResponse

List of text assistants response.

**Fields:**
- assistants: array of TextAssistantResponse (required)
- total: integer (required)

---

## TextAssistantResponse

Text assistant data response.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- name: string (required)
- is_active: boolean (required)
- agent_id: string | null
- linked_agent: LinkedAgentSummary | null
- active_tag: string | null
- system_prompt: string (required)
- greeting_message: string | null
- temperature: number (required)
- business_name: string | null
- industry: string | null
- mode: string (required)
- business_hours: object (required)
- timezone: string (required)
- enabled_channels: object (required)
- human_takeover_timeout_hours: integer (required)
- delayed_trigger_enabled: boolean (required)
- schedule_text_back_enabled: boolean
- ghl_integration_id: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- text_model: string
- followup_config: object | null
- created_at: string (required)
- updated_at: string (required)

---

## TextAssistantUpdate

Request body for updating a text assistant.

Allows changing operational settings and optionally the linked agent.
AI personality fields are managed through the linked agent.

**Fields:**
- name: string | null
- agent_id: string | null
- is_active: boolean | null
- active_tag: string | null — GHL contact tag that activates this assistant
- mode: string | null
- business_hours: object | null
- timezone: string | null
- enabled_channels: EnabledChannels | null
- human_takeover_timeout_hours: integer | null
- delayed_trigger_enabled: boolean | null
- schedule_text_back_enabled: boolean | null
- ghl_integration_id: string | null
- calendar_integration_id: string | null
- calendar_id: string | null
- text_model: string | null
- followup_config: object | null

---

## TextConversationListResponse

Response schema for listing conversations.

**Fields:**
- conversations: array of TextConversationResponse (required)
- total: integer (required)

---

## TextConversationResponse

Response schema for a text conversation.

**Fields:**
- id: string (required)
- tenant_id: string (required)
- text_assistant_id: string | null
- assistant_name: string | null
- assistant_names: array of string | null
- ghl_conversation_id: string | null
- contact_name: string | null
- ghl_contact_id: string | null
- channel: string (required)
- is_ai_active: boolean (required)
- last_inbound_at: string | null
- last_outbound_at: string | null
- last_human_reply_at: string | null
- message_count: integer | null
- function_call_count: integer | null
- created_at: string (required)
- updated_at: string | null

---

## TextDefaultsResponse

Response with default text assistant settings.

**Fields:**
- defaults: object (required)

---

## TextMessageListResponse

Response schema for listing messages in a conversation.

**Fields:**
- messages: array of TextMessageResponse (required)
- total: integer (required)

---

## TextMessageResponse

Response schema for a single text message.

**Fields:**
- id: string (required)
- conversation_id: string (required)
- role: string (required)
- content: string (required)
- function_calls: array of FunctionCallEntry | null
- channel: string | null
- created_at: string (required)

---

## TextPreviewPromptRequest

Request to preview the full generated text assistant prompt.

**Fields:**
- business_name: string (required)
- assistant_name: string
- industry: string
- description: string
- services: string
- pricing: string
- team: string
- faqs: string

---

## TextPreviewPromptResponse

Response with the full generated prompt and recommended settings.

**Fields:**
- system_prompt: string (required)
- greeting_message: string (required)
- recommended_settings: object (required)

---

## TierLimitsResponse

Current tier limits and usage for a tenant.

**Fields:**
- tier: string (required)
- agents: ResourceUsage (required)
- sub_accounts: ResourceUsage (required)
- team_members: ResourceUsage (required)
- share_links: ResourceUsage
- text_assistant_available: boolean
- demo_suite_available: boolean
- voice_rate_cents: integer
- premium_voice_rate_cents: integer

---

## TimelineEvent

Timeline event for user history.

**Fields:**
- event: string (required)
- label: string (required)
- timestamp: string (required)

---

## TwilioCredentialsRequest

Request schema for connecting Twilio account.

**Fields:**
- account_name: string (required) — Friendly name for this Twilio account
- account_sid: string (required) — Twilio Account SID (ACxxxxxx...)
- auth_token: string (required) — Twilio Auth Token

---

## UnreadCountResponse

Lightweight unread count for badge polling.

**Fields:**
- unread_count: integer (required)

---

## UpcomingInvoiceResponse

Upcoming invoice preview.

**Fields:**
- has_upcoming: boolean (required)
- amount_due: integer | null
- amount_due_formatted: string | null
- currency: string | null
- period_start: string | null
- period_end: string | null
- lines: array of object | null

---

## UpdateBrandingRequest

Request to update branding settings.

**Fields:**
- company_name: string | null
- primary_color: string | null
- support_email: string | null
- support_url: string | null

---

## UpdatePromptRequest

Request to update an existing system prompt using AI.

**Fields:**
- current_prompt: string (required) — The existing system prompt to modify
- instruction: string (required) — Instructions for how to modify the prompt
- functions: array of FunctionForUpdate — Optional: custom functions to integrate into the prompt
- quick_action: string enum ['integrate_functions', 'condense'] | null — Special action: 'integrate_functions' or 'condense'

---

## UpdatePromptResponse

Response with the updated system prompt and changes summary.

**Fields:**
- original_prompt: string (required)
- updated_prompt: string (required)
- changes_summary: string (required)
- changes_made: array of string (required)

---

## UpdateSubAccountRequest

Request to update a sub-account.

**Fields:**
- name: string | null
- admin_email: string | null
- admin_name: string | null
- per_minute_rate_cents: integer | null
- monthly_platform_fee_cents: integer | null
- is_active: boolean | null
- billing_start_day: integer | null
- upcharge_by_provider: object | null
- test_demo_upcharge_by_provider: object | null
- text_upcharge_by_type: object | null

---

## UpdateUserStatusRequest

Request to enable/disable a user.

**Fields:**
- disabled: boolean (required)

---

## UsageExportRecord

Single usage record for export - matches frontend AgencyUsageRecord.

**Fields:**
- id: string (required)
- sub_account_id: string (required)
- sub_account_name: string (required)
- sub_account_status: string
- call_log_id: string | null
- date: string (required)
- time: string | null
- direction: string
- minutes: integer (required)
- cost_cents: integer (required)
- revenue_cents: integer (required)
- margin_cents: integer (required)
- voice_provider: string

---

## UsageExportResponse

Usage export with records - matches frontend AgencyUsageResponse.

**Fields:**
- records: array of UsageExportRecord (required)
- total: integer (required)
- summary: UsageExportSummary (required)

---

## UsageExportSummary

Summary stats for usage export.

**Fields:**
- total_calls: integer (required)
- total_seconds: integer (required)
- total_cost_cents: integer (required)
- total_revenue_cents: integer (required)
- total_margin_cents: integer (required)
- by_provider: array of CostByProvider
- by_direction: array of CostByDirection

---

## UsageListResponse

Response containing list of usage records.

**Fields:**
- usage_records: array of UsageRecord (required)
- total_count: integer (required)
- total_minutes: number (required)
- total_cost_cents: integer (required)
- text_messages_count: integer
- text_messages_cost_cents: integer

---

## UsageRecord

Individual usage record.

**Fields:**
- id: string (required)
- call_log_id: string | null
- minutes: number (required)
- rate_cents: integer (required)
- total_cents: integer (required)
- synced_to_stripe: boolean (required)
- created_at: string (required)

---

## UsageSummary

Summary of usage for the current billing period.

**Fields:**
- current_period_start: string (required)
- current_period_end: string (required)
- total_minutes: integer (required)
- total_cost_cents: integer (required)
- calls_count: integer (required)
- text_messages_count: integer
- text_messages_cost_cents: integer

---

## UserAnalyticsAggregates

Aggregate analytics for dashboard charts.

**Fields:**
- kpis: AnalyticsKPIs (required)
- most_active: array of MostActiveUser (required)
- plan_distribution: array of PlanDistributionItem (required)
- churn_risk: array of ChurnRiskUser (required)
- signups_trend: array of ChartDataPoint (required)

---

## UserDetailCharts

Chart data for user detail view.

**Fields:**
- login_activity: array of ChartDataPoint (required)
- usage_trend: array of ChartDataPoint (required)

---

## UserDetailResponse

Full user detail with analytics.

**Fields:**
- user: UserDetailUser (required)
- tenant: UserDetailTenant (required)
- stats: UserStats (required)
- health: HealthScore (required)
- charts: UserDetailCharts (required)
- agents: array of AgentSummary (required)
- phone_numbers: array of PhoneNumberSummary (required)
- sub_accounts: array of app__admin__schemas__SubAccountSummary (required)
- timeline: array of TimelineEvent (required)

---

## UserDetailTenant

Tenant info for detail view.

**Fields:**
- id: string (required)
- name: string (required)
- plan: string (required)
- tenant_type: string (required)
- is_active: boolean (required)
- parent_tenant_id: string | null

---

## UserDetailUser

User info for detail view.

**Fields:**
- id: string (required)
- email: string (required)
- full_name: string | null
- role: string (required)
- created_at: string (required)

---

## UserListItem

User row with aggregated metrics for list view.

**Fields:**
- id: string (required)
- email: string (required)
- full_name: string | null
- role: string (required)
- created_at: string (required)
- tenant_id: string (required)
- tenant_name: string (required)
- plan: string (required)
- tenant_type: string (required)
- is_sub_account: boolean
- logins_24h: integer
- logins_7d: integer
- logins_30d: integer
- last_login: string | null
- production_minutes: number
- test_minutes: number
- phone_minutes: number
- call_count: integer
- agent_count: integer
- active_agents: integer
- phone_numbers: integer
- sub_accounts: integer
- health_score: integer (required)
- health_status: string enum ['healthy', 'warning', 'at_risk'] (required)
- signup_source: string | null
- referred_by_code: string | null

---

## UserResponse

User data response.

**Fields:**
- id: string (required)
- email: string (required)
- full_name: string | null
- role: string (required)
- tenant_id: string (required)
- created_at: string (required)
- is_super_admin: boolean

---

## UserStats

User statistics summary.

**Fields:**
- account_age_days: integer (required)
- total_minutes: number (required)
- total_calls: integer (required)
- logins_30d: integer (required)

---

## ValidationError

**Fields:**
- loc: array of string | integer (required)
- msg: string (required)
- type: string (required)
- input: ?
- ctx: object

---

## VariableDefinition

Definition for a template variable in agent prompts.

**Fields:**
- name: string (required) — Variable name (alphanumeric, underscore, hyphen)
- description: string | null — Description of what this variable represents
- required: boolean — Whether this variable must be provided at call time
- default_value: string | null — Default value if not provided (only for non-required)

---

## WebCrawlerCreate

Request body for creating a web crawler source.

**Fields:**
- name: string (required)
- root_url: string (required) — URL to crawl
- schedule_interval: string | null — Recrawl interval: 'daily', 'weekly', 'monthly', or None

---

## WebCrawlerResponse

Web crawler source response.

**Fields:**
- id: string (required)
- collection_id: string (required)
- name: string (required)
- source_type: string
- root_url: string (required)
- schedule_interval: string | null
- crawl_status: string
- pages_found: integer
- last_crawled_at: string | null
- next_crawl_at: string | null
- error_message: string | null
- document_id: string | null
- created_at: string (required)
- updated_at: string (required)

---

## WebCrawlerScheduleUpdate

Update the recrawl schedule for a web crawler.

**Fields:**
- schedule_interval: string | null — Recrawl interval: 'daily', 'weekly', 'monthly', or None

---

## WebhookCallContext

Optional context to pass to the agent for personalization.

**Fields:**
- first_name: string | null — Contact's first name
- last_name: string | null — Contact's last name
- email: string | null — Contact's email
- company: string | null — Contact's company
- source: string | null — Lead source (e.g., 'GHL Workflow', 'Website Form')
- notes: string | null — Additional context for the agent
- custom_fields: object | null — Custom key-value pairs

---

## WebhookSettingsResponse

Response for webhook settings.

**Fields:**
- webhook_url: string | null
- webhook_secret: string | null
- webhook_enabled: boolean
- ghl_conversation_sync_enabled: boolean

---

## WebhookTestContact

A GHL contact selected by the user to populate the test payload.

**Fields:**
- id: string (required)
- first_name: string | null
- last_name: string | null
- email: string | null
- phone: string | null
- company: string | null
- tags: array of string

---

## WebhookTestField

A single field definition for webhook test payload generation.

**Fields:**
- name: string (required)
- type: string (required)
- enum_values: array of string | null

---

## WebhookTestRequest

Request body for testing a webhook URL before creating a function.

**Fields:**
- webhook_url: string (required) — Webhook URL to test
- webhook_method: string — HTTP method for webhook call
- webhook_headers: object — Custom headers to include in webhook request
- webhook_timeout_ms: integer — Timeout for webhook call in milliseconds
- function_name: string | null — Function name to include in test payload
- fields: array of WebhookTestField | null — Configured fields to build sample arguments from
- contact: WebhookTestContact | null — GHL contact to populate call_context with real data

---

## WebhookTriggerRequest

Request body for webhook-triggered outbound calls.

Supports two formats:
- Direct: {"agent_id": "...", "to_number": "..."}  (n8n, Zapier, cURL)
- GHL:    {"customData": {"agent_id": "...", "to_number": "..."}, ...}

**Fields:**
- agent_id: string (required) — Agent ID to handle the call
- to_number: string (required) — Recipient phone number in E.164 format
- from_phone_number_id: string | null — Specific phone number to call from
- ghl_contact_id: string | null — GHL contact ID for pre-flight conversation checks
- context: WebhookCallContext | null — Context to personalize the call (injected into agent prompt)
- dynamic_variables: object | null — Variables to substitute in prompt: {'customer_name': 'John', 'order_id': '12345'}. All values must be strings.

---

## WebhookUrlTestRequest

Request to test a webhook URL directly (no demo ID needed).

**Fields:**
- webhook_url: string (required)
- form_fields: array of object | null

---

## app__admin__schemas__SubAccountSummary

Sub-account summary for user detail.

**Fields:**
- id: string (required)
- name: string (required)
- plan: string (required)
- created_at: string (required)

---

## app__agency__schemas__SubAccountSummary

Top sub-account stats for agency dashboard.

**Fields:**
- id: string (required)
- name: string (required)
- calls: integer (required)
- minutes: number (required)
- revenue_cents: integer (required)
- margin_cents: integer (required)
- conversion_rate: number (required)

---

## app__agents__prompt_router__GenerateAllKnowledgeRequest

Request to generate all knowledge sections at once.

**Fields:**
- business_name: string (required)
- industry: string (required)
- description: string — Business description for context
- agent_mode: string — Agent mode — outbound routes 'team' to objections generator

---

## app__agents__prompt_router__GenerateKnowledgeRequest

Request to generate a knowledge section using AI.

**Fields:**
- business_name: string (required)
- industry: string (required)
- section: string (required) — Section to generate: services, pricing, team, or faqs
- description: string — Business description for context
- services: string — Existing services list (for pricing/faqs context)
- agent_mode: string — Agent mode — outbound routes 'team' to objections generator

---

## app__text_assistant__prompt_router__GenerateAllKnowledgeRequest

Request to generate all knowledge sections at once.

**Fields:**
- business_name: string (required)
- industry: string (required)
- description: string — Business description for context

---

## app__text_assistant__prompt_router__GenerateKnowledgeRequest

Request to generate a knowledge section using AI.

**Fields:**
- business_name: string (required)
- industry: string (required)
- section: string (required) — Section to generate: services, pricing, team, or faqs
- description: string — Business description for context
- services: string — Existing services list (for pricing/faqs context)

---


# Demo Customization Reference

The `config` field on `DemoConfigCreate` / `DemoConfigUpdate` is an open `dict[str, Any]` in the API schema, but the frontend renderer reads a specific set of well-known keys to customize the public demo page. This appendix lists every key the renderer actually consumes, by channel.

These keys are not enforced by the OpenAPI schema — pass them in the `config` object of `POST /demos/` or `PATCH /demos/{demo_id}` and they will render. Unknown keys are stored but ignored.

---

## How to set a config key

```
POST /demos/
{
  "agent_id": "<uuid>",
  "channel": "phone",
  "name": "Acme Plumbing — Phone Demo",
  "config": {
    "phone_caller_image": "https://...supabase.co/storage/v1/object/public/...",
    "phone_accent_color": "#1d4ed8",
    "landing_heading": "Call Acme",
    "landing_subheading": "24/7 plumbing dispatch"
  }
}
```

Or update an existing demo:

```
PATCH /demos/{demo_id}
{ "config": { "phone_caller_image": "https://..." } }
```

To upload an image first (so you can reference its URL in `config`):

```
POST /demos/{demo_id}/upload-image
  multipart/form-data with file=<binary>
  → returns { "url": "https://...supabase.co/.../image.png" }
```

---

## Universal keys (apply to most channels)

| Key | Type | What it does |
|---|---|---|
| `display_name` | string | Overrides the agent's `agent_name` on the demo page. Useful when the prospect's brand persona differs from the internal agent name. |
| `landing_heading` | string | Large headline shown above the start-call button on the landing screen. |
| `landing_subheading` | string | Secondary text under the heading. |
| `landing_instructions` | string | Short text telling the visitor how to interact ("Click Start, then ask about pricing"). |
| `calendar_embed_url` | string (URL) | A calendar booking page to embed in the post-call CTA panel. Takes priority over `after_cta_url` when set. |
| `embed_show_transcript` | boolean | When true, the live transcript renders inside the iframe alongside the demo UI. Defaults false. |

---

## Phone channel (`channel: "phone"`)

The iPhone-mockup demo (incoming call → in-call). Reads:

| Key | Type | What it does |
|---|---|---|
| `phone_caller_image` | string (URL) | Image displayed in the circular avatar inside the iPhone mockup. Defaults to initials of `business_name` or `display_name`. Set this to a public URL (uploadable via `/demos/{id}/upload-image`). |
| `phone_accent_color` | string (hex) | Accent color for the call-arc rings, "Incoming call…" pill highlight, and the answer-button glow. Defaults to Leadlock blue (`#3b82f6`). |

---

## Orb / web channels (`channel: "orb"`, `channel: "web"`)

The default voice-only showpiece demo. Reads:

| Key | Type | What it does |
|---|---|---|
| `orb_theme` | string (preset name) | Visual theme preset for the orb (e.g. `default`, `aurora`, `pulse`). |
| `orb_custom_color` | string (hex) | Custom accent color for the orb when not using a preset. |
| `orb_position` | string | Orb placement on screen (e.g. `center`, `bottom-right`). |

---

## Messenger channel (`channel: "fb_messenger"`, `channel: "ig_messenger"`)

Facebook / Instagram Messenger chat UI mockup. Reads:

| Key | Type | What it does |
|---|---|---|
| `avatar_url` | string (URL) | Contact avatar image shown in the chat header. |
| `display_name` | string | Contact name shown in the chat header (also covered above). |
| `status_text` | string | Online status / activity text ("Active now", "Typically replies in 5 min"). |
| `accent_color` | string (hex) | Chat bubble + accent color. Defaults to `#0084FF` (Messenger blue). |

---

## WhatsApp / SMS / TikTok channels

Text-channel chat UI mockups. Read:

| Key | Type | What it does |
|---|---|---|
| `avatar_url` | string (URL) | Contact avatar. |
| `display_name` | string | Contact name in the chat header. |
| `status_text` | string | Online status text (WhatsApp / IG / TikTok only). |

---

## Lead form channel (`channel: "fb_lead"`, `channel: "ig_lead"`)

Facebook / Instagram lead-ad → form → call flow. Reads:

| Key | Type | What it does |
|---|---|---|
| `ad_headline` | string | Headline on the ad mockup. |
| `ad_body` | string | Body copy on the ad mockup. |
| `ad_image_url` | string (URL) | Hero image on the ad mockup. |
| `avatar_url` | string (URL) | Brand avatar shown in the form header. |
| `business_name` | string | Business name shown in the form. |
| `display_name` | string | Same as `business_name` for cases that distinguish. |
| `cta_button_text` | string | CTA button label on the ad ("Get Quote", "Book Now"). |
| `form_title` | string | Form headline. |
| `form_subtitle` | string | Sub-headline under the form title. |
| `form_fields` | array of objects | Fields to render (`name`, `phone`, `email`, etc.). |

---

## Embedding the demo in another site

The public demo page at `https://app.leadlock.ai/d/<slug>` supports query parameters for iframe embedding:

| Query param | Effect |
|---|---|
| `?embed=true` | Sets the page background to **transparent** on `html`, `body`, and `#root`, and applies a compact, fit-to-viewport layout. The parent page's background color shows through the iframe — use this to embed in a light-themed site (white surround), a dark site, or any branded color. |
| `?vid=<visitor_id>` | First-party visitor identity, captured from the parent page's localStorage via the embed script. Carried into call records so you can stitch demo activity to the same visitor across sessions. |
| `?gcid=<ghl_contact_id>` | GoHighLevel contact ID. When the parent page is a GHL funnel and the visitor is a known contact, this links demo calls to the GHL contact record. |

### Embed examples

White-themed parent site (the surround will be white):
```html
<iframe
  src="https://app.leadlock.ai/d/<slug>?embed=true"
  width="100%" height="700"
  style="border: none; background: white;">
</iframe>
```

Dark-themed parent site (default appearance — the iframe's transparent background shows the parent's dark color):
```html
<iframe
  src="https://app.leadlock.ai/d/<slug>?embed=true"
  width="100%" height="700"
  style="border: none;">
</iframe>
```

Stitched to a known GoHighLevel contact:
```html
<iframe
  src="https://app.leadlock.ai/d/<slug>?embed=true&gcid={{contact.id}}"
  width="100%" height="700"
  style="border: none;">
</iframe>
```

---

## Common recipes

### Drop a prospect's logo into a phone demo

```
1. POST /demos/{demo_id}/upload-image  (file=prospect-logo.png)
   → { "url": "https://...supabase.co/storage/.../prospect-logo.png" }

2. PATCH /demos/{demo_id}
   { "config": { "phone_caller_image": "<url from step 1>" } }
```

### Match a prospect's brand color on a phone demo

```
PATCH /demos/{demo_id}
{ "config": { "phone_accent_color": "#1d4ed8" } }
```

### Embed in a GoHighLevel landing page with white surround

```html
<iframe src="https://app.leadlock.ai/d/<slug>?embed=true"
        width="100%" height="700" style="border: none;"></iframe>
```

### Full per-prospect customization (phone channel)

```
PATCH /demos/{demo_id}
{
  "config": {
    "display_name": "Acme Plumbing",
    "phone_caller_image": "https://...supabase.co/.../acme-logo.png",
    "phone_accent_color": "#FF5722",
    "landing_heading": "Try Acme's 24/7 AI dispatcher",
    "landing_subheading": "Ask about a clogged drain or a busted water heater",
    "landing_instructions": "Click Start, then talk like you're a homeowner with an urgent plumbing issue."
  }
}
```

---
