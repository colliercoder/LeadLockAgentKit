# Access Control
Source: https://docs.retellai.com/accounts/access-control

Manage users and access of your workspace, invite and remove user.

To keep your workspace safe, we have RBAC (Role Based Access Control) system.

### System Roles

#### Admin

Full control over workspace resources and members. Complete access to all features including billing, user management, and workspace settings.

Can:

* Invite, remove, and change roles for members
* View and manage billing: usage, invoices, payment methods, subscriptions, and customer portal
* Create, edit, and delete agents, conversation flows, Retell LLMs, knowledge bases, voices, and folders
* Configure developer settings
* Access all data, including raw transcripts and recordings
* Manage telephony settings
* Update or delete the workspace

Cannot:

* None — Admins have full permissions

#### Developer

Full functional access to build and test agents, view raw data, manage analytics and developer settings. Cannot manage billing or organization users.

Can:

* Build and edit agents, flows, LLMs, KBs, voices
* Test and simulate; manage test cases and playground
* View raw logs, transcripts, recordings, and analytics
* Create exports; run calls and batch calls
* Manage API/public keys and webhooks; adjust concurrency/CPS

Cannot:

* Manage billing (usage, invoices, payment methods, subscriptions)
* Invite, remove, or change member roles
* Update or delete the workspace

#### Member

Read-only access to agents, testing artifacts, scrubbed history, and analytics. Cannot make changes or view sensitive data.

Can:

* View agents and configurations (read‑only)
* View tests, playground threads, and analytics
* View scrubbed history; batch calls and phone resources
* List workspace members

Cannot:

* Create, edit, or delete resources
* Start calls/chats, run simulations, or change playground
* Access API/public keys, webhooks, or raw transcripts/recordings
* Manage billing, settings, or team members

### Invite User

Now under the user management of your workspace, you (admin) can invite user with a specific role.

<Frame>
  <img alt="invite_user.jpeg" />
</Frame>

### Change User Role

You can change the role of active users in the workspace.

<Frame>
  <img alt="update_user_role.jpeg" />
</Frame>

### Remove User

You can also remove user from your workspace.


# Account
Source: https://docs.retellai.com/accounts/account

Manage your Retell AI account, reset passwords, and delete account.

To keep your information safe, we use **Auth0** as our login system.

## Account Status

Your account could have the following statuses:

* **Active**: Your account is active and all services are available.
* **Verification Needed**: Your account is on hold for further verification due to high volume calls, please contact [support@retellai.com](mailto:support@retellai.com) with your company's name, use case, and verification that you represent the company.
* **Invoice Past Due**: Your account has a past due invoice and is at risk of automatic shutdown in 7 days. Please make a payment to keep your service active.
* **Invoice Overdue**: Your account has an overdue balance, and your service has been temporarily deactivated. Please make a payment to restore your service.

## Reset your password

If you want to change or reset your password:

1. Go to the login page.
2. Click the **"Don’t remember your password?"** link.
3. Enter your email address and follow the instructions sent to your inbox.

For better security, we recommend using **Sign in with Google**. This provides an extra layer of protection and reduces the need to manage separate passwords.

<Frame>
  <img alt="Login page with the password reset link highlighted" />
</Frame>

### Important Note About SSO and Password-Based Sign-In

Please note that **Google SSO** and **email-password sign-in** are treated as **separate accounts** in our system. They are not automatically linked.

If you currently use one sign-in method (e.g., **email-password sign-in**) and wish to switch to the other (e.g., **Google SSO**), follow these steps:

1. Log in to your account using your current method (either Google SSO or email-password sign-in).
2. Click your profile photo at the bottom left of the dashboard.
3. Navigate to **"Workspace"** and send an invite to your email address.
4. Log out of your current account.
5. Open the invite email and use the **alternative sign-in method** to create a new account (e.g., sign in with Google if you currently use email, or sign up with email and password if you currently use Google SSO).

This will create a separate account with the new sign-in method while maintaining access to your existing workspace.

## Delete your account

If you are deleting the only workspace in the account, the account will be deleted automatically. Before proceeding:

* Ensure you have downloaded any important data you wish to keep
* Check that all pending invoices are settled
* Cancel any active subscriptions
* Remove any connected third-party integrations

<Note>
  Account deletion is permanent and cannot be undone. All associated data, including billing history and user preferences, will be permanently removed.
</Note>

<Frame>
  <img alt="Workspace settings page with the delete workspace button" />
</Frame>

<Frame>
  <img alt="Delete account" />
</Frame>


# Add payment methods
Source: https://docs.retellai.com/accounts/add-payment

Add a payment method via Stripe to continue using Retell services after the trial.

Adding a payment method is required before you can purchase phone numbers or use Retell services after the trial period. We use Stripe to securely process all payments.

## Adding Your Payment Method

<Steps>
  <Step title="Navigate to Billing">
    Go to the Billing tab in your dashboard

    <Frame>
      <img alt="Billing tab in the dashboard" />
    </Frame>
  </Step>

  <Step title="Access Payment Settings">
    Click "Change payment methods" to open payment settings

    <Frame>
      <img alt="Change payment methods button" />
    </Frame>
  </Step>

  <Step title="Add New Payment Method">
    In the Stripe portal, click "Add payment method" and enter your payment details. Your payment information is securely handled by Stripe.

    <Frame>
      <img alt="Stripe payment details form" />
    </Frame>
  </Step>
</Steps>


# API Key Overview
Source: https://docs.retellai.com/accounts/api-keys-overview

Authenticate API requests and secure webhooks using API keys.

API keys are used to authenticate your requests to:

* REST API endpoints
* SDK integrations
* Webhook endpoints

Each workspace can have multiple API keys, all sharing the same permission level.

### REST API Authentication

To authenticate your REST API requests, include your API key in the request headers:

```http theme={null}
Authorization: Bearer YOUR_API_KEY
```

Try out authentication in our [API Playground](/api-references/create-phone-call) to see it in action.

### Webhook API Key

For enhanced security, we automatically designate one of your API keys for [webhook authentication](/features/secure-webhook). This designated webhook API key:

* Is used to sign and verify webhook requests
* Cannot be deleted
* Ensures your webhook endpoints only receive legitimate requests

<Note>
  Keep your API keys secure and never share them in public repositories or client-side code.
</Note>


# Billing Overview
Source: https://docs.retellai.com/accounts/billing

Learn how to monitor your workspace's usage, manage your subscription, and update billing information.

## Billing Overview

The Billing tab allows you to manage payments, track expenses, and download invoices. Here's what you can do:

1. Payment Management: We use Stripe for secure and reliable payment processing. You can update your payment methods by clicking on the "Change payment methods" button.
2. Billing History: Review your monthly expenses, including detailed cost breakdowns by category (e.g., Voice Infra, LLM).
3. Invoices: Easily download invoices by clicking the "Invoice" button next to the respective period.
4. Current Charges: View ongoing costs for the current billing period, including itemized amounts and usage details.

<Frame>
  <img alt="billing_1.png" />
</Frame>

## View usage breakdown

The Usage tab on Billing page provides a clear breakdown of your workspace’s activity and costs. Here’s what you can track:

1. Total Cost: Your total expenses for the selected billing period.
2. Call Minutes: The total number of call minutes used.
3. Average Cost Per Minute: The average cost for each minute of calls.
4. Daily or weekly call costs, making it easy to identify high-cost periods and track spending trends over time.
5. Cost by Provider: A detailed breakdown of expenses across providers, such as voice infra, large language models (LLMs), telephony services, and concurrency usage.

<Frame>
  <img alt="billing_1.png" />
</Frame>


# Exceptions to Our Per-Minute Pricing
Source: https://docs.retellai.com/accounts/billing-exceptions

Learn about billing adjustments for dynamic opening messages and long token prompt lengths that may affect your call costs.

## Overview

While we generally bill based on actual call duration, certain call characteristics may result in adjusted billing to ensure fair pricing for our services.

## Rule 1: Minimum Duration for Dynamic Opening Messages

**When it applies:** Calls shorter than 10 seconds that use dynamic opening messages when AI speaks first

**Billing adjustment:** Minimum charge of 10 seconds

<Frame>
  <img alt="Dynamic Message - AI Speaks first" />
</Frame>

**Example:**

* Call duration: 6 seconds
* Dynamic opening messages: Enabled
* Billed duration: 10 seconds (4 seconds additional charge)

**Why:** Dynamic opening messages require processing time regardless of call length, so we ensure a minimum charge to cover these costs.

## Rule 2: LLM Price Scaling for > 3,500 Token Prompt Length

**When it applies:** Agents that use more than 3,500 LLM tokens in their prompts

**Billing adjustment:** Duration is scaled proportionally based on token usage

**What's included in token calculation:**

* global prompt
* functions (tool descriptions)
* state / node prompt
* transcript between agent and user
* tool call history and results

<Note>
  [Flex mode](/build/conversation-flow/flex-mode) is a common trigger for this rule.
  It compiles all node prompts, transitions, and tool descriptions into a single LLM
  context, which can push the token count well above 3,500.
</Note>

**Price calculation:**

* Scaling Factor = Prompt LLM Tokens ÷ 3,500
* Billed Duration = Original Duration × Scaling Factor (rounded up)

**Example:**

* Call duration: 60 seconds
* LLM tokens used: 4,200
* Scaling factor: 4,200 ÷ 3,500 = 1.2
* Billed duration: 72 seconds (12 seconds additional charge)

<Frame>
  <img alt="Long token prompts pricing in dashboard" />
</Frame>

**Why:** Larger LLM prompt lengths incurs greater costs due to token-based pricing from our underlying model providers, so we scale the billing accordingly to reflect these increased expenses.


# Data Retention Policy
Source: https://docs.retellai.com/accounts/data-retention

Configure automatic data deletion periods for call and chat data.

# Data Retention Policy

Retell allows you to configure a data retention period per agent. After the retention period expires, call and chat data associated with that agent is automatically and permanently deleted.

By default, data is kept indefinitely (no automatic deletion).

## How It Works

* Data retention is configured **per agent** under Security & Fallback Settings
* Expired data is automatically deleted on a daily basis
* Deletion is **permanent and irreversible** — deleted data cannot be recovered
* Applies to both voice calls and chats

<Frame>
  <img alt="Retention dropdown showing available retention period options" />
</Frame>

## How to Configure

1. Navigate to your agent
2. Open **Security & Fallback Settings**
3. Under **Data Storage Settings**, select your preferred data storage mode
4. Use the **Retention** dropdown to set how long data is kept before automatic deletion

The retention period applies regardless of which data storage mode you select (Everything, Everything except PII, or Basic Attributes Only).

## What Gets Deleted

When the retention period expires, the following data is permanently removed:

* **Call recordings** (audio files)
* **Transcripts**
* **Call and chat logs**
* **Knowledge base retrieval logs**
* **Dynamic variables and metadata**

While some basic metadata is retained internally, the call or chat is effectively deleted and will no longer appear in session history or API responses.

<Warning>
  Deletion is irreversible. Make sure to export any data you need before the retention period expires. You can use [webhook events](/features/webhook-overview) to capture call data in real time, or use the [Get Call](/api-references/get-call) / [Get Chat](/api-references/get-chat) API to retrieve data before it expires.
</Warning>

## Available Retention Periods

| Option       | Duration                        |
| ------------ | ------------------------------- |
| Keep forever | No automatic deletion (default) |
| 1 day        | 24 hours after call/chat starts |
| 3 days       |                                 |
| 7 days       |                                 |
| 30 days      | 1 month                         |
| 60 days      | 2 months                        |
| 90 days      | 3 months                        |
| 180 days     | 6 months                        |
| 365 days     | 1 year                          |
| 730 days     | 2 years                         |

## API Configuration

You can set the retention period via the API when creating or updating an agent:

```json theme={null}
{
  "data_storage_retention_days": 90
}
```

* **Field**: `data_storage_retention_days`
* **Type**: integer (1–730) or `null`
* **Default**: `null` (keep forever)

See the [Update Agent](/api-references/update-agent) or [Create Agent](/api-references/create-agent) API reference for details.

## Related

* [Data Storage Settings](/accounts/privacy-disable) — control what types of data are stored
* [Secure URLs](/accounts/signed-secure-url) — configure URL expiration for recordings and logs


# Handle failed payments
Source: https://docs.retellai.com/accounts/fail-payment

Resolve failed payments by checking with your bank or updating your payment method.

If your payment fails, follow these steps to resolve the issue:

<Steps>
  <Step title="Check with Your Bank">
    1. Contact your bank to ensure the transaction isn't being blocked
    2. Request to allowlist transactions from Retell
    3. Return to the Retell Dashboard and retry the payment
  </Step>

  <Step title="If Payment Still Fails">
    1. Obtain written confirmation from your bank that Retell has been allowlisted
       * Statement should be on bank letterhead
       * Should explicitly confirm that transactions from Retell are now approved
    2. Email the statement to [support@retellai.com](mailto:support@retellai.com)
    3. Include your Retell account details in the email
  </Step>

  <Step title="Alternative Payment Method">
    1. Consider adding a different payment method
    2. Go to the "Billing" tab
    3. Click "Change payment methods"
    4. Add a new card or payment method
  </Step>
</Steps>

If you continue experiencing issues, please contact our support team via the [Customer Support Portal](https://support.retellai.com/) or at [support@retellai.com](mailto:support@retellai.com) for further assistance.


# KYC Verification
Source: https://docs.retellai.com/accounts/kyc

Complete KYC verification to enable outbound calls on Retell.

Before you can make outbound calls with Retell, you’ll need to complete KYC (Know Your Customer) verification. Depending on your account information, there are a few ways to pass KYC.

### How to Pass KYC

#### Automatic verification

We may automatically verify your account based on the information you provided during registration. If this applies, your KYC will be approved without any additional steps.

#### Verification via Persona

If automatic verification is not possible, you will be asked to complete KYC through Persona using your government-issued ID.

You can go to “Phone Numbers”, click on any of your numbers, and you’ll see the interface where you can start the KYC process.

<Frame>
  <img alt="KYC verification section on the phone number page" />
</Frame>

We currently support verification in 83 countries.

If your country is not listed, please contact us — we will review your case based on risk and business needs and may enable verification for your country.

### ID Verification Restrictions

Each person can verify only one account. Our system detects duplicate identities, so even using a different government ID may be flagged as a duplicate. If your previous account was verified and later deleted, contact our support team to request a manual review.


# Manage API Keys
Source: https://docs.retellai.com/accounts/manage-api-keys

Manage your API keys for authentication, webhooks.

The "API Keys" section is belong to System "Settings". The "API Keys" section allows you to manage your authentication credentials for accessing the API. Here's what you can do:

1. **Create a new API key**
   * Click the "Add" button
   * Give your key a descriptive name to identify its purpose

2. **Delete an existing API key**
   * Locate the key you want to remove
   * Click the delete (trash) icon
   * Confirm the deletion when prompted

3. **Set a webhook API key**
   * Select an existing API key
   * Click "Set as Webhook Key" to designate it for webhook authentication
   * Only one key can be set as the webhook key at a time

<Note>
  Keep your API keys secure and never share them publicly. If a key is compromised, delete it immediately and create a new one.
</Note>

<Frame>
  <img alt="API Keys management interface" />
</Frame>


# Data Storage Settings
Source: https://docs.retellai.com/accounts/privacy-disable

Manage your data storage privacy settings and choose how sensitive data is stored.

# Data Storage Privacy Settings

By default, we store these potentially sensitive data related to your calls, including:

* Call logs
* Transcriptions
* Call recordings
* Caller ID for inbound call
* Callee ID for outbound call
* Knowledge base retrieved contents logs
* Dynamic variables
* Metadata

## How to Manage Data Storage

You can opt out of sensitive data storage at any time:

1. Navigate to your agent
2. Under **Security & Fallback Settings → Data Storage Settings**, select:
   * **Everything** — store transcripts, recordings, and logs
   * **Everything except PII** — store content, excluding PII when possible
   * **Basic Attributes Only** — store only metadata (no transcripts/recordings/logs)

<Frame>
  <img alt="Privacy settings showing Data Storage Settings options" />
</Frame>

<Note>
  You can also configure a **data retention period** to automatically delete stored data after a set number of days. See [Data Retention Policy](/accounts/data-retention) for details.
</Note>

## What Happens When You Change Storage Settings

When you opt out:

* You will continue to receive [webhook events](features/webhook-overview), where you can access the transcript, call recording, and other sensitive data in it
  * The call recording link will expire after 10 minutes upon receiving the webhook
* **Everything**: All artifacts (transcripts, recordings, logs) are stored
* **Everything except PII**: Artifacts are stored with PII removed according to the categories you select in your `pii_config`. See [PII scrubbing](#pii-scrubbing) below for exactly which fields are affected.
* **Basic Attributes Only**: No transcripts/recordings/logs are stored; if you query the call with the get call API later, you will not get these fields

## PII scrubbing

When you choose "Everything except PII", you can configure which personally identifiable information (PII) is removed after the call completes. Scrubbing is applied across the **transcript, recording, public logs, and structured fields on the call record itself** (dynamic variables, metadata, call analysis, tool call arguments and results).

PII configuration is defined on the agent. Per-call storage behavior can still be limited via `data_storage_setting` inherited onto the call.

### Content categories

When any of these categories are selected, occurrences are detected post-call and replaced with `[category number]` placeholders (e.g. `[email 1]`, `[person name 2]`):

* `person_name`
* `address`
* `email`
* `ssn`
* `passport`
* `driver_license`
* `credit_card`
* `bank_account`
* `password`
* `pin`
* `medical_id`
* `date_of_birth`
* `customer_account_number`

These placeholders are written into the scrubbed copies of:

* **Transcript** — user and agent utterances
* **Recording** — audio is replaced with a beep over the PII intervals (surfaced as `scrubbed_recording_url`)
* **Public logs** — log file content
* **Dynamic variables** — `retell_llm_dynamic_variables`, collected dynamic variables, and override dynamic variables (surfaced as their `scrubbed_*` counterparts)
* **Metadata** — `metadata` (surfaced as `scrubbed_metadata`)
* **Call analysis** — `call_analysis.call_summary` and `call_analysis.custom_analysis_data` (surfaced as `scrubbed_call_analysis`)
* **Tool calls** — arguments and results
* **DTMF digits** — replaced with `[PII INFO]` whenever any PII category is enabled, to avoid exposing touch-tone passwords or PINs
* **SMS message text** (for chat agents)

The raw originals are deleted under "Everything except PII" — only the scrubbed versions remain.

### `phone_number` (directional)

`phone_number` behaves differently from the content categories. Selecting it redacts the **customer's** phone number from the call record itself, not just the transcript:

* **Inbound calls**: `from_number` is removed
* **Outbound calls**: `to_number` is removed
* **SMS chats**: `user_number` is removed

The opposite-direction number (your Retell number) is preserved. The field is removed entirely from the call object — there is no placeholder. If you need to keep the customer's number visible for downstream systems, do not include `phone_number` in your categories.

### What is always preserved

Regardless of the categories you configure, these fields are never altered or removed by PII scrubbing:

* **Identifiers**: `call_id`, `agent_id`
* **Timing**: `start_timestamp`, `end_timestamp`, `duration_ms`
* **Outcome**: `call_status`, `disconnection_reason`, `call_successful`, `user_sentiment`, `in_voicemail`
* **Operational**: `direction`, `transfer_destination`, `call_latency`, `cost_metadata`, `call_cost`, `custom_attributes`
* **Tool call records** — the name, timing, and success of each tool call (their *arguments and results* are still scrubbed when content categories are selected)

To remove these fields as well, use the **Basic Attributes Only** storage setting or configure a [data retention period](/accounts/data-retention).

<Frame>
  <img alt="PII scrubbing configuration" />
</Frame>

<Frame>
  <img alt="Example of PII scrubbing result" />
</Frame>


# Public Keys
Source: https://docs.retellai.com/accounts/public-keys



## Overview

Public keys are specifically designed for authenticating the Retell Chat Widget when embedded on your website. Unlike API keys, which should never be exposed in client-side code, public keys are safe to include in frontend applications for this specific purpose.

Public keys are used exclusively for:

* Embedding the [Retell Chat Widget](/deploy/chat-widget) on your website

<Frame>
  <img alt="Public key management page" />
</Frame>

## Allowed Domains

For security reasons, public keys are restricted to specific domains. This prevents unauthorized use of your public key on other websites.

To configure allowed domains:

1. Navigate to the **Public Keys** section in your Retell dashboard
2. Click on the public key you want to configure
3. Add the domains where your public key can be used (e.g., `example.com`, `app.example.com`)
4. Save your changes

<Note>
  **Testing on localhost**

  To test your integration locally, add `localhost` to your allowed domains list. This enables development and testing on your local machine before deploying to production.
</Note>

## Google reCAPTCHA v3 Protection (Optional)

You can optionally enable Google reCAPTCHA v3 protection for your public key to prevent abuse when using the Retell Chat Widget. When enabled, the chat widget will require reCAPTCHA verification before initiating conversations.

To enable reCAPTCHA:

1. Navigate to the **Public Keys** section in your Retell dashboard
2. Click on the public key you want to configure
3. Toggle on **Abuse Prevention (Google reCAPTCHA)**
4. Add your reCAPTCHA Secret Key (obtain from [Google's reCAPTCHA page](https://www.google.com/recaptcha))
5. Adjust the Score Threshold (default: 0.5)
   * Lower scores are more likely to be bots
   * Higher thresholds may block more real users
6. Save your changes

<Note>
  When reCAPTCHA is enabled for a public key, you must also implement reCAPTCHA on your frontend. See [Google's reCAPTCHA documentation](https://developers.google.com/recaptcha/docs/v3) for implementation details.
</Note>

## Security Considerations

While public keys are specifically designed for use with the Retell Chat Widget in client-side code, you should still follow these best practices:

* Only add domains you control to the allowed domains list
* Regularly review your allowed domains to ensure they're up-to-date
* Use the most restrictive domain settings possible for your use case
* For server-to-server communication, use [API keys](/accounts/api-keys-overview) instead

## Managing Public Keys

You can create, view, and manage your public keys from the Retell dashboard:

1. Navigate to the **Public Keys** section
2. Create a new public key or select an existing one to configure
3. Set up allowed domains as needed
4. Copy the public key to use with the Retell Chat Widget on your website


# Opt in to secure URL
Source: https://docs.retellai.com/accounts/signed-secure-url



# Secure URL

By default, the URLs we generate for call recordings and logs do not expire, allowing you to easily share the links with other people.
However, if security is a concern and you want to prevent unauthorized access in case the URL is leaked, you can opt in for secure URLs.
Secure URLs automatically expire 24 hours after they are generated, providing an additional layer of security.

## How to Opt In

You can opt in to secure URLs at any time:

1. Navigate to your agent
2. Toggle the "Opt In Secure URL" switch

<Frame>
  <img alt="Privacy settings showing the Opt In Secure URL toggle" />
</Frame>

## What Happens When You Opt In

* Every time you request the URLs of your call's recording and log, we will generate a URL with a signature that will expire 24 hours after it is generated.
* Accessing the resource using the URL after 24 hours will be denied.
* Files created before secure URLs were enabled will still be generated without signatures.

## What Happens When You Opt Out After Opt In

* Files created while secure URLs were enabled will continue to generate signed URLs with 24-hour expiration whenever you request their URLs, even after you opt out.
* Only files created after you opt out will generate non-expiring URLs.


# Workspace
Source: https://docs.retellai.com/accounts/workspace

Create, manage, and collaborate in workspaces, including team invites and deletion.

Learn how to create and manage workspaces, and collaborate with team members.

## Default Workspace

When you first create an account, a default workspace is automatically created for you. This workspace serves as your primary environment for managing projects and collaborating with team members.

## Find your Workspace id / org id

Sometimes we might ask for your workspace id / org id when debugging issues related to your account. You can find it in your workspace settings page.

<Frame>
  <img alt="Settings page entry in the sidebar" />
</Frame>

You can access your workspace setting in system settings page:

<Frame>
  <img alt="Workspace settings page" />
</Frame>

And retrieve the workspace id here:

<Frame>
  <img alt="Workspace ID location in settings" />
</Frame>

## Creating Additional Workspaces

To create a new workspace:

1. Click the workspace selector in the top left corner of the dashboard
2. Select "Add another workspace"
3. Enter your workspace name
4. Click "Save"

<Frame>
  <img alt="Creating a new workspace" />
</Frame>

## Managing Team Members

### Inviting Members

To invite team members to your workspace:

1. Click the "Workspace" button in the bottom left corner
2. Navigate to the "Members" tab
3. Click "Invite Members"
4. Enter the email addresses of team members
5. Click "Send"

If a team member does not receive the invitation email, you can resend it by clicking the "Invite Members" button again, re-entering their email address, and clicking "Send".

<Frame>
  <img alt="Workspace settings page" />
</Frame>

<Frame>
  <img alt="Workspace members list with invite option" />
</Frame>

### Invitation Process

* Invited members will receive an email with a link to join the workspace
* They can create a new account or use an existing one
* Once accepted, they'll have immediate access

<Frame>
  <img alt="Pending member invitations" />
</Frame>

## Leave a Workspace

To leave a workspace:

1. Navigate to the workspace settings page
2. Click the Options menu (three dots) button against your name
3. Select "Leave workspace"
4. Confirm your action

**Important considerations before leaving:**

* You can only leave a workspace if there is at least one other member remaining
* If you are the only member in the workspace, you must delete the workspace instead
* You can rejoin the workspace if another member invites you back

<Frame>
  <img alt="Leave workspace option in the member menu" />
</Frame>

## Delete Workspace

In the workspace settings page, you can delete the workspace by clicking the "Delete" button. Before deletion, please note:

* All workspace data will be permanently deleted and cannot be recovered
* A final invoice will be generated and charged for any usage up to the deletion date
* All team members will lose access to the workspace
* Any active API keys will be invalidated

<Frame>
  <img alt="Delete workspace confirmation dialog" />
</Frame>


# Set language for your agent
Source: https://docs.retellai.com/agent/language



You can set a specific language for an agent. The language setting affects three things during a call:

* **Speech recognition** — which language the agent transcribes the caller from.
* **Voice pronunciation** — the language the voice uses to pronounce words and shape its accent.
* **Agent text** — the agent is automatically instructed to respond in the configured language. You do **not** need to add a "respond in X" instruction to your prompt.

The voice you select is still the primary determinant of accent — the language setting refines pronunciation rules and ensures the right speech recognition model is used.

## Pick a single language (recommended)

A single-language agent is the most accurate setup: the agent transcribes in one language only, the voice speaks with that language's pronunciation, and the agent always responds in that language — no language detection involved.

<img />

If no language is selected, the agent defaults to **English (US)**.

The chosen voice must support the chosen language. The dashboard hides unsupported combinations from the picker, with a tooltip explaining which voice or voice model is blocking it.

## Need more than one language?

<Card title="Configure a multilingual agent" icon="globe" href="/agent/multilingual">
  For agents that serve callers in different languages, see the multilingual guide.
</Card>

If you already know the caller's language at call time (for example, from CRM context or the dialed number), prefer overriding the language per call via the [inbound call webhook](/features/inbound-call-webhook). This gives you single-language accuracy on each call without limiting which customers the agent can serve.

## Supported languages

The language you pick must be supported by both your chosen **voice provider** (for pronunciation) and at least one **speech recognition provider** (for transcription). The combinations change as providers add coverage, so the dashboard is the source of truth.

On any agent page, open the language picker — the dropdown shows the live set of supported languages and updates as you change the voice provider, voice (and pinned voice model), and ASR provider. The same picker works in both single-language and multiselect modes. Unsupported combinations are greyed out, with a tooltip explaining which selection is blocking each one.

Still picking your stack? See the [TTS provider comparison](/build/tts-provider-comparison) and [ASR provider comparison](/build/asr-provider-comparison) for provider-level coverage and trade-offs.

For locale variants (for example, British English vs. US English, European Spanish vs. Latin American Spanish), the dashboard's language picker exposes the specific dialect codes when supported.


# Configure a multilingual agent
Source: https://docs.retellai.com/agent/multilingual

Pick the specific languages your agent should support, and understand the accuracy trade-offs.

Use a multilingual agent when callers may speak in different languages and you can't determine which language ahead of time. If you can determine the language at the start of a call (for example, from CRM context or the dialed number), you'll get better accuracy by keeping the agent single-language and overriding the language per call via the [inbound call webhook](/features/inbound-call-webhook).

## Granular language selection

In the dashboard, switch the language selector to **Multiselect** and pick the exact set of languages the agent should support — for example, English (US) + Spanish (Spain).

<img />

What happens at call time:

* **Speech recognition** — the agent figures out which of the selected languages the caller is speaking and transcribes accordingly.
* **Voice pronunciation** — the agent detects the language of each response and uses the matching pronunciation. If detection fails, it falls back to the first language you selected. Not all voice providers handle accents.
* **Agent text** — the agent is allowed to respond in any of the selected languages and chooses based on what the caller speaks (and any instructions you give in the prompt).

## Accuracy trade-offs

<Note>
  Selecting multiple **variants of the same base language** (for example, `en-US` and `en-GB`) does **not** trigger the multilingual speech-recognition pipeline. The agent stays on the single-language path for that base, with no accuracy penalty.

  Crossing language families (for example, `en-US` and `es-ES`) routes speech recognition to the multilingual pipeline, which is less accurate per language than single-language models. Pick the smallest set of languages you actually need.
</Note>

From most to least accurate:

1. **Single language** — best accuracy. Use this whenever you can.
2. **Multiple variants of the same base language** (e.g., `en-US` + `en-GB`) — same accuracy as single language for that base.
3. **Multiple languages across families** (e.g., `en-US` + `es-ES`) — multilingual pipeline; some accuracy loss per language.
4. **Legacy Multilingual setting** — static list of supported languages, see below.

## Legacy Multilingual setting

Older agents may still have the generic **Multilingual** setting selected. It is preserved so existing agents keep working, but the dashboard now flags it as a legacy setting:

> "Multilingual" is a legacy setting. Pick specific languages to update.

<img />

The legacy Multilingual setting covers these ten languages only: English (US), Spanish (ES), French (FR), German (DE), Hindi (IN), Russian (RU), Portuguese (PT), Japanese (JP), Italian (IT), Dutch (NL).

For new agents, pick the specific languages you need instead — narrower sets are more accurate.

## Picks the dashboard won't allow

Some combinations are blocked at selection time:

* **Voice doesn't support a language.** Each voice (and pinned voice model) only supports a subset of languages. Unsupported combinations are greyed out in the language picker, with a tooltip explaining which voice or voice model is blocking it. Pick a different voice to enable that language.
* **No speech-recognition provider covers the combination.** Some combinations of languages have no single speech-recognition provider that covers all of them together. The dashboard greys those languages out with the reason — either drop a language or split the use case across multiple agents.


# Setup versioning and tags for agents
Source: https://docs.retellai.com/agent/version



Versioning lets you update an agent while keeping other versions unchanged for production use.

It has two main purposes:

1. **Lock in configuration**: published versions cannot be changed, and you can attach specific versions to phone numbers or environment tags to lock in the agent configuration.
2. **Version control & history**: you can create multiple draft versions from any past version, track your version history, and publish any draft when it's ready.

## How version numbers work

Version numbers start at **V0** and go up by one each time you create a new version. The dashboard labels tell you whether a version is live or still in progress.

| UI                            | Meaning                                                                                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `V0`, `V1`, `V2`, …           | **Published** versions, immutable                                                                                                               |
| `V3 (draft)`, `V4 (draft)`, … | **Draft** versions — unpublished copies that reserve the next version number. The **(draft)** suffix means you can still edit and publish them. |

**Example flow**

1. You publish your first agent → **V0** appears under **Published**.
2. You create a new draft from V0 → the UI shows **V1 (draft)** under **Draft**.
3. You publish that draft → **V1** moves to **Published** and is no longer editable.
4. You create another draft from V1 → **V2 (draft)** appears under **Draft**.

Multiple drafts can exist at the same time (for example **V2 (draft)** and **V3 (draft)**). Each version also shows which version it was branched from.

<Note>
  Published versions cannot be changed. Only versions labeled with **(draft)** can be edited.
</Note>

## How to manage versions

Click the version button in the upper right corner of the agent page to open the versions panel.

<Frame>
  <img />
</Frame>

The panel shows two sections:

* **Draft**: unpublished versions that can still be edited.
* **Published**

<Frame>
  <img />
</Frame>

Versions with attached environment tags (e.g. `prod`, `staging`) are shown inline on the version entry.

### Create a new draft

Click the **+** button in the versions panel to create a new draft from the currently selected version. The draft will show which version it was branched from.

### Publish a draft

You can publish any draft version. Select the draft in the versions panel, then click the **Publish** button in the upper right corner.

<Frame>
  <img />
</Frame>

After clicking **Publish**, a modal appears where you can add an optional version name and description. You can also check **Auto Create a New Draft** to automatically create a new draft version after publishing.

<Frame>
  <img />
</Frame>

To attach phone numbers to a version, use the **Phone Numbers** tab in the dashboard.

### Delete a version

To delete a draft or published version, open the versions panel, select the version, and use the delete option. Published versions with active phone numbers or environment tags attached should have those removed before deleting.

## Environment Tags

<Frame>
  <img />
</Frame>

Environment tags store environment-specific configs. Apply a tag (e.g. `prod`, `staging`) to a version to instantly load the right settings — and move the tag to a different version to deploy without manually rerouting phone numbers, dynamic variables, etc.

A version can have multiple tags attached.

### How environment tags work

Each agent comes with `prod` and `staging` tags by default. You can create up to **10 tags total** per agent (including the defaults).

Tags serve two purposes:

1. **Labels** — tags appear directly on version entries in the panel, so you can see at a glance which versions are running in which environments (e.g. which version is `prod`, which is `staging`).

2. **Environment-specific config** — each tag carries its own set of dynamic variable values. When a tag is active on a version, those values are automatically injected, so the same agent behaves correctly across environments without duplicating configuration.

To deploy a new version, move the tag from the old version to the new one. Phone numbers, webhooks, and anything else pointing to that tag switch over instantly — no manual rerouting needed.

### Configure tags

Click the **Environment** button in the agent header to apply a tag to the current version, or select **Configure Tags** to manage your tags.

<Frame>
  <img />
</Frame>

<Frame>
  <img />
</Frame>

In the **Configure Environment Tags** modal you can:

* Create a new tag by clicking **+ Add** in the left sidebar and giving it a name.
* Define **environment dynamic variables** — key/value pairs that are injected into the agent when that tag is active. This lets the same agent behave differently across environments without duplicating configuration.

**Tag name requirements**

* Up to 20 characters
* May contain lowercase letters, numbers, `-`, or `_`
* Must start with a lowercase letter
* Cannot be `latest`
* Cannot match the pattern `v` followed by numbers only (e.g. `v3`, `v12`)

### Applying tags to a version

To attach a tag to a version, select the version in the versions panel, then click the **Environment** button and choose the tag. The tag label will appear on the version entry in the panel.

## How to use versions and tags in the API

You can pass a version reference in API calls such as `get_agent`, `get_retell_llm`, `create_web_call`, and `create_phone_number`.

A version reference can be:

* A version number, such as `2`
* `latest`
* An environment tag, such as `prod` or `staging`

When you pass an environment tag, Retell uses the version currently assigned to
that tag and applies the tag's dynamic variables. If the tag exists but is not
assigned to a version, Retell uses the latest version.

If you do not pass a version reference, the Retell SDK defaults to the latest
version of the agent.

<CodeGroup>
  ```typescript Node theme={null}
  // Gets the version with version number 2.
  const agent = await client.agent.retrieve("agent_id", { version: 2 });

  // Gets the version assigned to the prod tag.
  const prodAgent = await client.agent.retrieve("agent_id", { version: "prod" });

  // Starts a web call with the version assigned to the staging tag.
  const webCall = await client.call.createWebCall({
    agent_id: "agent_id",
    agent_version: "staging",
  });

  // Gets the latest version of the agent.
  const latestAgent = await client.agent.retrieve("agent_id");
  ```

  ```python Python theme={null}
  # Gets the version with version number 2.
  agent = client.agent.retrieve("agent_id", version=2)

  # Gets the version assigned to the prod tag.
  prod_agent = client.agent.retrieve("agent_id", version="prod")

  # Starts a web call with the version assigned to the staging tag.
  web_call = client.call.create_web_call(
      agent_id="agent_id",
      agent_version="staging",
  )

  # Gets the latest version of the agent.
  latest_agent = client.agent.retrieve("agent_id")
  ```
</CodeGroup>


# Compare agent versions
Source: https://docs.retellai.com/agent/version-comparison

Compare any two versions of an agent to see what changed between them.

You can compare any two versions of an agent to see exactly what changed between them. This is useful for reviewing changes before publishing, auditing past modifications, or understanding the differences between versions.

## How to Access Version Comparison

There are two ways to open the version comparison modal:

1. **From Version History**: Click the clock icon to open version history, hover over a version, and click the "Compare versions" button. This will compare the selected version against the current draft.

2. **From Publish Modal**: When publishing a new version, click the "Compare" button in the publish modal to see what's changing between the last published version and your current draft.

<img />

## Comparison Modes

The version comparison feature offers two different view modes to help you understand changes:

### Standard View (JSON Diff)

The standard view shows a traditional diff view with the full JSON configuration of both versions side by side.

<img />

**Features:**

* **Split view**: Shows the two versions in separate columns for easy comparison
* **Syntax highlighting**: JSON syntax is color-coded for readability
* **Show parent fields**: Toggle this option to see the parent JSON structure containing changes, making it easier to understand the context of modifications

### Semantic Diff

The semantic diff view provides a more human-readable summary of changes, organizing them by field.

<img />

**Features:**

* **Change summary**: Shows a count of additions, removals, and modifications at the top
* **Categorized by change type**: Changes are categorized as added (+), removed (−), or changed (\~)
* **Field paths**: Each change shows the full path to the modified field (e.g., `response_engine.prompt`)
* **Expandable details**: Click on complex values to expand and see the full content
* **Word-level diffs**: For long text changes, highlights the specific words that were added or removed

<Tip>
  Use **Standard View** when you need to see the complete configuration context or verify exact JSON structure. Use **Semantic Diff** when you want a quick, scannable summary of what changed.
</Tip>

## What Gets Compared

When comparing versions, the modal shows differences across all components of your agent:

* **Agent configuration**: Basic agent settings and metadata
* **Response Engine**: For single/multi prompt agents, shows Retell LLM changes. For conversation flow agents, shows flow configuration changes
* **Related entities**: Any linked knowledge bases, functions, or other configurations


# Address Metric Issues
Source: https://docs.retellai.com/ai-qa/address-metric-issues

How to fix common metric issues surfaced by AI QA

## Overview

When AI QA analyzes your calls, it flags specific metrics that didn't meet expectations. This page provides actionable guidance for addressing each type of metric issue to improve your agent's performance. For detailed definitions of each metric, see [AI QA metrics](/ai-qa/terminologies).

## AI Accuracy

### High Agent Hallucination Rate

When the agent generates incorrect or fabricated information not supported by the conversation context or knowledge base.

**How to fix:** Use the call QA sheet to see whether each instance is Fabrication, Contradiction, or Confusion, then apply the right fix:

* **Fabrication** (inventing facts): Add the correct information to your knowledge base or system prompt so the agent has it instead of guessing
* **Contradiction** (conflicting with provided info): Simplify or clarify conflicting instructions in your system prompt
* **Confusion** (misunderstanding user intent): Break complex instructions into simpler steps, or use conversation flow nodes with focused prompts

### Low KB (Knowledge Base) Recall

When relevant knowledge base chunks are not being retrieved when they should be.

**How to fix:**

* Reduce the KB retrieval threshold and increase the number of chunks to reduce false negatives (missed relevant chunks)
* Adjust these in your agent's [Knowledge Base](/build/knowledge-base) configuration; make small changes and monitor impact in later QA runs

## Response-engine issues

### High Node Transition Inaccuracy

When node transitions are inaccurate, the agent is moving to the wrong conversation state. This problem is specific to conversation flow agents, because only that engine type uses nodes and transitions between them.

**How to fix:**

* Clarify the transition conditions in your conversation flow node prompts
* Add examples that demonstrate the correct transition behavior for edge cases
* Keep transition prompts unambiguous and avoid overlapping conditions between nodes; see the [conversation flow debug guide](/build/conversation-flow/debug-guide) for a step-by-step walkthrough

### High Tool Call Inaccuracy

When the agent calls the wrong tools, misses required tool calls, or passes incorrect arguments. This problem is specific to single-prompt and multi-prompt agents, because only those engine types decide freely when and which tools to call.

**How to fix:**

* In your agent prompt, spell out when to call which tools (and when not to)
* In your [tool definitions](/build/add-function-calling), use clear names and descriptions and add examples for parameters so the agent can choose and invoke tools correctly

<Info>
  Tool Call Inaccuracy measures whether the agent made the right **decision** about which tools to call and with what arguments. For issues with tool **execution** failing (e.g., endpoint errors), see [Custom Tool Failures](#custom-tool-failures) below.
</Info>

## Speech Quality

### Poor Agent Naturalness

When the agent sounds unnatural — issues like mispronunciation, robotic pacing, or audio artifacts.

**How to fix:**

* **Change voice**: Custom-cloned voices tend to have more naturalness issues; switching to a platform voice often improves stability
* **Adjust voice temperature**: Change the temperature setting to affect vocal expressiveness
* **Switch voice provider**: Different providers have different strengths (e.g., naturalness vs. specific languages or accents)

### Poor Agent Sentiment

When the agent's responses carry negative or inappropriate emotional tone.

**How to fix:**

* Adjust your system prompt with explicit tone guidelines (e.g., "respond warmly and helpfully")
* If using a conversation flow, check whether any node prompts produce overly terse or cold responses
* Reword dismissive phrases (e.g., "I can't help with that" → "Let me find another way to help")

## Transcription Quality

### High Word Error Rate (WER)

When the speech-to-text transcription has a high error rate, causing the agent to misunderstand what the user said.

**How to fix:**

* **Switch STT provider**: Choose a higher-accuracy speech-to-text provider for your use case
* **Check language settings**: Ensure the language setting matches the actual spoken language — mismatched settings significantly increase WER
* **Add custom vocabulary**: If your STT provider supports it, add frequently used names, technical terms, or domain-specific words as boosted keywords
* **Use Mistranscribed Entities feedback**: Review the mistranscribed entities surfaced by AI QA and add those specific terms as [boosted keywords](/reliability/wrong-transcript) in your STT configuration
* **Reduce background noise**: If the call environment is too noisy, try turning on background removal to improve transcription accuracy

## User Experience

### High User Negative Sentiment

When multiple user utterances show negative sentiment, the agent may not be handling the conversation well.

**How to fix:**

* Adjust your agent's system prompt to encourage more empathetic, friendly responses
* Add instructions for handling frustrated users (e.g., acknowledge concerns before offering solutions)

### High Overlapping Speech Count

Frequent overlapping speech may indicate latency or responsiveness issues. The fix depends on whether latency is also a problem:

| Scenario                          | How to fix                                                                                                                                                           |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **High latency (e2e p50 > 2.5s)** | Fix latency first. Choose faster models and lower-latency voice providers. When the agent takes too long to respond, users are more likely to talk over it.          |
| **Normal latency**                | Decrease agent responsiveness or increase interruption sensitivity. The agent may be starting to speak too quickly or not detecting when the user wants to continue. |

## Tool Execution

### Custom Tool Failures

When custom tool calls fail during a call.

**How to fix:**

* Check your tool endpoint logs for the failing call to see the specific error
* Ensure endpoints handle edge cases and return appropriate error responses
* Verify that tool response formats match the expected schema
* Add timeout handling and retry logic where appropriate; see [Function calling](/build/add-function-calling) for endpoint setup details

<Info>
  This metric measures whether your tool endpoints executed successfully. For issues with the agent choosing the wrong tools to call, see [High Tool Call Inaccuracy](#high-tool-call-inaccuracy) above.
</Info>

### Transfer Call Issues

When transfer calls fail.

**How to fix:**

* Check the error log for the specific error — it usually indicates the cause
* **Telephony issues** (e.g. connection or configuration): Change the relevant settings or contact your telephony provider to resolve
* **No one picking up**: Review staffing levels during peak times; verify transfer destination numbers and that someone is available to receive the call
* **Human detection not working**: If you use [Warm Transfer](/build/conversation-flow/call-transfer-node) and the system fails to detect when a human has answered, try switching to [Agentic Warm Transfer](/build/conversation-flow/call-transfer-node), which uses a transfer agent to converse with the transfer target before bridging.

## Performance

### High Latency

When end-to-end latency is too high (e.g., p50 exceeds 2.5 seconds).

**How to fix:**

* Use the [latency breakdown](/reliability/troubleshoot-latency) in the call dashboard to find the bottleneck (LLM inference, TTS, network, etc.)
* If LLM inference is the bottleneck, switch to a faster model
* If TTS is the bottleneck, choose a lower-latency voice provider
* If tool calls are slow, optimize tool endpoints or reduce response size

## Custom Evaluation

### Failed Custom Evaluation Criteria

When one or more AI Evaluated Conditions fail.

**How to fix:**

* Use the failure reason in the call QA sheet to identify the gap, then update your agent's system prompt or knowledge base as needed
* If the failure was actually correct behavior (e.g., intentional by design), use [calibration](/ai-qa/terminologies#calibration) to override the evaluation for that call

<Info>
  Not all failures are actionable — some may be caused by external factors (e.g., the user hanging up early) or intentional design decisions (e.g., transferring when a user requests a human). Focus on failures where the agent's behavior or configuration can be improved.
</Info>

**Calibration best practices:**

* Use calibration to correct edge cases where the automatic evaluation doesn't match your judgment
* If you find yourself calibrating many calls the same way, update your resolution criteria or metric thresholds instead — this is more efficient and applies to all future evaluations
* Add notes when calibrating to document why the override was needed, which helps your team maintain consistency

## Interpreting Your Results

<Tip>
  When interpreting metrics, consider them in context:

  * Compare metrics across similar cohorts or time periods
  * Look for trends rather than focusing on individual data points
  * Use multiple metrics together to get a complete picture of call quality
</Tip>


# Define QA Cohort
Source: https://docs.retellai.com/ai-qa/create-cohort



<Frame>
  <img alt="QA cohort creation form" />
</Frame>

<Steps>
  <Step title="Cohort Name">
    The **Cohort Name** field is where you define a unique identifier for your QA cohort. This name helps you organize and identify different cohorts in your AI QA dashboard.

    * **Best Practice**: Use descriptive names that indicate the purpose or criteria of the cohort (e.g., High-Value Customers Q4, Support Calls - Week 1)
  </Step>

  <Step title="Filter Calls by Agent and Criteria">
    This section allows you to define which calls should be included in your cohort based on multiple filtering criteria.

    **1. Agents**

    The **Agents** dropdown lets you select one or more agents whose calls you want to analyze.

    * **Use Case**: Analyze performance across specific agents, compare agent performance, or focus on a particular agent's calls

    **2. Date Range**

    The **Date Range** fields allow you to specify a time period for the calls you want to include in your cohort.

    * **Start Date**: Required. Sets the beginning of the date range for calls to include in the cohort.
    * **End Date**: Optional. If omitted, the cohort will continuously add new calls that match the other criteria as they occur, creating a dynamic cohort that updates over time.

    **3. Call Duration**

    The **Call Duration** filter lets you include or exclude calls based on their length.

    * **Use Case**:
      * Filter out very short calls (e.g., > 30 seconds) that may not be meaningful
      * Focus on longer calls that require more analysis
      * Identify calls that are too short or too long

    **4. Disconnection Reason**

    You can filter calls by various [disconnection reasons](/reliability/debug-call-disconnect).

    **5. Post Call Analysis**

    The **Post Call Analysis** filter allows you to add custom filters based on post-call analysis results.
  </Step>

  <Step title="Set Sampling Percentage">
    This section controls how many calls from your filtered set will actually be analyzed, helping you manage analysis volume and costs.

    #### Percentage

    The **Percentage** field determines what percentage of calls matching your filters will be included in the cohort.

    * **Example**: Setting 50% means half of all calls matching your filters will be analyzed

    #### Weekly Max

    The **Weekly Max** field sets a maximum number of calls that can be analyzed per week.

    * **Example**: Setting the Weekly Max to 100 ensures that no more than 100 calls are included in the cohort each week, even if the percentage filter would otherwise allow more.

    <Note>
      The Weekly Max acts as a cap. If your percentage calculation results in fewer calls than the Weekly Max, the percentage takes precedence. If it results in more, the Weekly Max limit applies.
    </Note>
  </Step>

  <Step title="Click Next to Continue">
    After configuring your cohort filters and sampling options, select the **Next** button to proceed.
  </Step>
</Steps>


# Define Resolution Criteria
Source: https://docs.retellai.com/ai-qa/define-resolution-criteria



<Frame>
  <img alt="resolution_criteria.png" />
</Frame>

## What Determines a Successful Call?

The **"What determines a successful call?"** question is the core of defining resolution criteria. This step allows you to set up the evaluation framework that determines whether calls in your cohort are considered successful or not.

<Steps>
  <Step title="AI Evaluated Condition">
    The **AI Evaluated Condition** section allows you to define custom criteria that are evaluated by AI based on call transcripts and context.

    **Name**

    The **Name** field is a short identifier for your condition (e.g., "Call resolved", "Customer satisfied", "Issue escalated properly").

    **Prompt Description**

    The **Prompt Description** is the actual prompt that the AI uses to evaluate whether the condition is met for each call.

    * **Example**: "AI agent was able to resolve user's query"
    * **Best Practice**:
      * Be specific about what success looks like
      * Include relevant context about the call type or use case
      * Use clear, unambiguous language

    You can add multiple AI Evaluated Conditions by clicking the **"+ Add"** button. Each condition will be evaluated independently, and you can delete any condition using the trash icon.
  </Step>

  <Step title="Performance Metric">
    The **Performance Metric** section allows you to define quantitative thresholds that calls must meet to be considered successful.

    ### Metrics

    The **Metric** dropdown lets you select which performance metric to evaluate:

    * **Latency**: Measures the end-to-end delay between a user speaking and the Voice AI beginning its spoken response.
    * **User Sentiment**: Represents the emotional state of the caller as inferred from speech content, tone, and pitch.
    * **Agent Sentiment**: Represents the emotional tone expressed by the Voice AI during speech output.
    * **Overlapping Speech**: Count of times the user and agent spoke at the same time.
    * **Transcription**: WER and number of mistranscribed entities.
    * **Agent Hallucination**: Measures how often the agent hallucinated.
    * **Tool Call Inaccuracy**: Measures the rate at which the agent invoked incorrect tools.
    * **Node Transition Inaccuracy**: Measures incorrect node transitions.
    * **Agent Naturalness**: Measures how human-like the agent sounded, including pronunciation, intonation, pacing, turn-taking behavior, and the absence of robotic patterns.

    ### Example Configuration

    <Frame>
      <img alt="performance-metric.png" />
    </Frame>

    You can add multiple Performance Metrics by clicking the **"+ Add"** button.

    <Note>
      Both AI Evaluated Conditions and Performance Metrics are evaluated. A call is considered successful only if it meets all defined criteria across both sections.
    </Note>
  </Step>

  <Step title="Weighted Scoring (Advanced)">
    The **Weighted Scoring** toggle enables you to assign different weights to your resolution criteria, allowing you to give more weight to certain conditions or metrics over others.

    * **When Enabled**: You can assign weights to each AI Evaluated Condition and Performance Metric. Set the Success Criteria threshold.
    * **When Disabled**: All criteria are treated equally - a call must meet all conditions to be considered successful

    <Frame>
      <img alt="resolution-criteria-weighted.png" />
    </Frame>

    <Tip>
      Use weighted scoring when some criteria are more important than others. For example, you might weight "Call resolved" higher than "Customer satisfaction" if resolution is your primary goal.
    </Tip>
  </Step>

  <Step title="Save and Run QA">
    After configuring your resolution criteria, complete the process by clicking the **Save and Run QA** button.

    <Warning>
      If you encounter an error when saving, review your conditions and metrics to ensure all required fields are filled and criteria thresholds are set. Resolve any validation messages before retrying.
    </Warning>
  </Step>
</Steps>


# Get Started
Source: https://docs.retellai.com/ai-qa/get-started



To get started, click on the **AI QA** tab in the left sidebar. This will take you to the AI QA dashboard where you can view existing cohorts or create new ones.

<Frame>
  <img alt="AI QA tab in the left sidebar navigation" />
</Frame>

A **cohort** is a group of calls that you evaluate together using the same set of rules and metrics. Each cohort defines which calls to include (by agent, date range, or other filters) and what criteria to assess them against, so you can track quality trends and compare performance across different slices of your call traffic.

To create a new QA cohort, click the **Create QA** button at the top right of the AI QA page.

<Frame>
  <img alt="AI QA dashboard with the Create QA button at the top right" />
</Frame>


# AI Quality Assurance
Source: https://docs.retellai.com/ai-qa/overview

Analyze AI calls with structured insights across audio, language, and performance.

## What is AI QA?

AI QA (Quality Assurance) automatically evaluates a sampled set of calls using configurable rules and metrics. It surfaces high-level trends (scores, resolution rate, latency) and deep, call-level diagnostics (hallucinations, knowledge base accuracy, overlapping speech, sentiment, and tool usage).

## Use AI QA to:

* Track call quality and resolution over time
* Identify failure patterns and root causes
* Review individual calls with transcript-level evidence

<Frame>
  <img alt="advanced_qa.png" />
</Frame>

## Pricing

<Tip>
  For each workspace, AI QA is free for the first 100 minutes of usage.
</Tip>

After the free usage, AI QA is priced at \$0.10 per minute of analyzed call time.


# AI QA Metrics
Source: https://docs.retellai.com/ai-qa/terminologies

Detailed definitions of every metric and term used in AI QA call analysis

## Overview

This page explains every metric and term used in AI QA so you can interpret your call analysis results. For each metric, you’ll see what it measures and how it’s evaluated. When a metric fails your criteria, use [Address metric issues](/ai-qa/address-metric-issues) to find step-by-step guidance on how to fix it.

## Performance Metrics

### Latency

**Average Latency**: Measures the end-to-end delay between a user speaking and the Voice AI beginning its spoken response. Lower latency indicates more responsive interactions.

**Latency P50**: The 50th percentile (median) of latency measurements. This metric shows the typical response time, with half of all responses being faster and half being slower.

<Info>
  Latency is measured in seconds (s). Lower values indicate better performance.
</Info>

### Sentiment Analysis

**User Sentiment**: Represents the emotional state of the caller as inferred from speech content, tone, and pitch. Sentiment can be positive, negative, or neutral.

* **User Positive Sentiment Rate**: Percentage of user interactions with positive sentiment
* **User Negative Sentiment Rate**: Percentage of user interactions with negative sentiment
* **Negative Sentiment Rate**: Overall rate of negative sentiment detected in the conversation

**Agent Sentiment**: Represents the emotional tone expressed by the Voice AI during speech output. This metric helps ensure your agent maintains an appropriate tone throughout conversations.

* **Agent Positive Sentiment Rate**: Percentage of agent responses with positive sentiment
* **Agent Natural Tonality Rate**: Measures how natural and human-like the agent's tone sounds

### Transcription Metrics

**WER (Word Error Rate)**: Measures the accuracy of speech-to-text transcription by calculating the percentage of words that were incorrectly transcribed. Lower WER indicates better transcription accuracy.

<Note>
  WER is calculated as: (Substitutions + Insertions + Deletions) / Total Words in Reference × 100%
</Note>

<Accordion title="How is the WER reference transcript generated?">
  The reference is produced by re-transcribing the user's audio using a process that listens to the audio and uses the original STT transcript as reference. This usually yields a much more accurate transcript than the initial STT output, though the reference can still contain errors.

  WER measures how much the original STT transcript diverges from this reference.
</Accordion>

**Mistranscribed Entities**: Count of specific entities (names, dates, numbers, etc.) that were incorrectly transcribed during the call. Only critical factual errors that change meaning are counted.

### Call Quality Metrics

**Overlapping Speech**: Count of times the user and agent spoke at the same time during the conversation. Higher counts may indicate the agent is speaking too long or not responding appropriately.

**Avg. Overlapping Speech**: Average number of overlapping speech instances per call across the cohort.

**Agent Naturalness**: Measures how human-like the agent sounded, including pronunciation, intonation, pacing, turn-taking behavior, and the absence of robotic patterns. Higher values indicate more natural-sounding speech.

<Accordion title="How is Agent Naturalness evaluated?">
  Agent Naturalness is evaluated using **both the audio and the transcript**. The evaluation looks for issues that would affect how understandable or natural the agent sounds, such as:

  * Robotic glitches, distortion, or unexpected volume changes
  * Mispronunciation or word substitution that differs from what was intended
  * Slurring, mumbling, or dropped sounds
  * Speech speed or intonation that sounds unnatural or alters meaning

  Only clear issues that would confuse a listener are flagged; minor robotic tone or technical phrasing is not counted against the metric.

  **Natural Tonality Rate** = (utterances without naturalness issues / total agent utterances) × 100%
</Accordion>

**Natural Tonality Rate**: Percentage of agent speech that sounds natural and human-like in tone and delivery.

### AI Accuracy Metrics

**LLM Hallucination Rate**: Measures how often the Large Language Model (LLM) generated incorrect or fabricated information that wasn't supported by the conversation context or knowledge base.

**Agent Hallucination**: Measures how often the agent hallucinated during conversations. This is a critical metric for ensuring factual accuracy.

<Accordion title="How is Hallucination Rate calculated?">
  Hallucination is evaluated **per agent turn** — each response is checked against the agent's instructions, knowledge base, and conversation history. The rate is the percentage of agent turns that contain a hallucination.

  **Types of hallucination:**

  * **Fabrication**: Invents factual claims not supported by the context (e.g., making up a case number)
  * **Contradiction**: States something that conflicts with what was provided or said earlier
  * **Confusion**: Misunderstands instructions and gives factually irrelevant or logically wrong information

  Severity can be **major** (critical false information that could cause a failed resolution) or **minor** (non-critical discrepancies). The evaluation focuses on factual accuracy only, not style or tone.
</Accordion>

<Warning>
  High hallucination rates indicate the agent may be providing incorrect information to users, which can damage trust and lead to poor outcomes.
</Warning>

### Knowledge Base Metrics

**KB (Knowledge Base) Recall**: Measures how effectively the agent retrieved and used relevant information from the knowledge base. Higher recall indicates better knowledge base utilization.

<Accordion title="How is KB Recall calculated?">
  KB Recall is evaluated per retrieval turn. For each turn where the knowledge base is queried, the system determines which retrieved chunks were truly relevant to the user's question.

  * A **"Hit"** (full recall) means all relevant chunks were retrieved for that turn
  * A **"Miss"** means one or more relevant chunks were missed

  **KB Recall Rate** = (turns with full recall / total retrieval turns) × 100%

  Relevance is judged strictly: a chunk counts as relevant only if it provides specific, actionable information or instructions that apply to what the user was asking, not general or marketing-style content.
</Accordion>

### Tool and Function Metrics

**Tool Call Accuracy**: Measures the rate at which the agent correctly invoked tools or functions. Higher accuracy means the agent is using the right tools at the right time.

**Tool Call Inaccuracy**: Measures the rate at which the agent invoked incorrect tools. This is the inverse of Tool Call Accuracy.

**Custom Tool Success Rate**: Percentage of custom tool calls that completed successfully.

**Avg Custom Tool Latency**: Average time taken for custom tools to execute and return results.

### Conversation Flow Metrics

**Transition Accuracy**: Measures the accuracy of transitions between conversation nodes or states. Higher accuracy indicates the agent is following the intended conversation flow correctly.

**Node Transition Inaccuracy**: Measures incorrect node transitions in conversation flows. This metric helps identify when the agent moves to the wrong conversation state.

### Call Resolution Metrics

**Call Resolution Rate**: Percentage of calls that were successfully resolved according to your defined resolution criteria.

**Average Score**: Overall quality score for calls in the cohort, calculated based on your resolution criteria and weighted scoring configuration.

**Calls Analyzed**: Total number of calls that have been analyzed in the cohort.

### Transfer Metrics

**Transfer Success Rate**: Percentage of calls that were successfully transferred to another agent or system.

**Transfer Wait Time**: Average time users wait before a transfer is completed.

## Call-Level Data

### Call Identification

**Call ID**: Unique identifier for each individual call in the system.

**Call Start Time**: Timestamp indicating when a call began.

**Call Length**: Total duration of the call, typically measured in seconds or minutes.

### Evaluation Status

**Eval**: Evaluation status or score for individual calls, indicating whether the call met the defined resolution criteria.

## Statistical Terms

### Percentiles

**P50 (50th Percentile)**: The median value, where half of all measurements are above and half are below. Also known as the median.

<Info>
  Percentiles help understand the distribution of metrics. P50 shows typical performance, while P95 or P99 show worst-case scenarios.
</Info>

## Cohort Terms

### Cohort

A **Cohort** is a filtered set of calls that share common characteristics (agents, date range, call duration, etc.) and are analyzed together using the same resolution criteria.

### Sampling

**Sampling Percentage**: The percentage of calls matching your filters that will be included in the cohort for analysis.

**Weekly Max**: Maximum number of calls that can be analyzed per week, regardless of the sampling percentage.

## Resolution Criteria Terms

### AI Evaluated Condition

Custom criteria evaluated by AI based on call transcripts and context. These are qualitative assessments (e.g., "Call resolved", "Customer satisfied") rather than quantitative metrics.

### Performance Metric

Quantitative thresholds that calls must meet, such as latency below 2 seconds or sentiment above 80%.

### Weighted Scoring

A scoring system that assigns different weights to various resolution criteria, allowing you to prioritize certain conditions or metrics over others.

### Calibration

**Calibrate to Success / Calibrate to Failure**: Manual overrides that let you adjust automatic metric evaluations for a specific call.

<Accordion title="How does calibration work?">
  * **Calibrate to Success**: Mark a failed metric as passed — the failure no longer counts against the call's score
  * **Calibrate to Failure**: Mark a passed metric as failed — the pass no longer contributes to the call's score

  **Important:** Calibration updates the **per-call score only**. It does **not** change the underlying metric criteria or scoring logic for future calls. Each calibration applies to the specific call you are reviewing.
</Accordion>

<Warning>
  Some metrics may show "N/A" when there isn't sufficient data or when the metric doesn't apply to a particular call type (e.g., transfer metrics for non-transfer calls).
</Warning>


# View QA Results
Source: https://docs.retellai.com/ai-qa/view-qa-results

Analyze call quality metrics, review individual calls, and access detailed QA diagnostics for your cohort

## Overview

The QA Results dashboard provides comprehensive insights into your call quality through two main views: **Call QA Overview** for high-level trends and metrics, and **Detailed Calls** for individual call analysis. You can drill down into specific calls to review detailed QA diagnostics, errors, and transcripts.

## Accessing QA Results

After creating a QA cohort and running analysis, navigate to your cohort to view the results. The dashboard displays:

* **Summary metrics** across all analyzed calls
* **Trend charts** showing performance over time
* **Individual call records** with detailed evaluation scores
* **Call-level QA sheets** with transcript analysis and error details

## Call QA Overview Tab

The **Call QA Overview** tab provides a high-level view of your cohort's performance with interactive charts and summary metrics.

### Summary Metrics

The top section displays key performance indicators (KPIs) in a grid layout:

* **Calls Analyzed**: Total number of calls analyzed in the cohort
* **Average Score**: Overall quality score based on your resolution criteria
* **Call Resolution Rate**: Percentage of calls successfully resolved
* **Transfer Success Rate**: Percentage of calls that were successfully transferred to another agent or system
* **Transfer Wait Time**: Average time users wait before a transfer is completed
* **Average Latency**: Mean response time across all calls
* **LLM Hallucination Rate**: Percentage of calls with AI-generated inaccuracies
* **KB (Knowledge Base) Recall**: Knowledge base retrieval effectiveness
* **Negative Sentiment Rate**: Percentage of interactions with negative sentiment
* **WER (Word Error Rate)**: Transcription accuracy
* **Avg. Overlapping Speech**: Average number of overlapping speech instances per call
* **Tool Call Accuracy**: Rate of correct tool/function invocations
* **Transition Accuracy**: Accuracy of conversation flow transitions
* **Agent Natural Tonality Rate**: Percentage of natural-sounding agent speech
* **Agent Positive Sentiment Rate**: Percentage of agent responses with positive sentiment
* **Avg Custom Tool Latency**: Average time taken for custom tools to execute and return results
* **Custom Tool Success Rate**: Percentage of custom tool calls that completed successfully

<Frame>
  <img alt="Trend charts for various performance metrics" />
</Frame>

### Top Questions from Users

The dashboard includes a table showing the most frequently asked questions by users, along with resolution rates:

<Frame>
  <img alt="Top questions from users with resolution rates" />
</Frame>

AI QA intelligently groups similar questions to provide a consolidated view.
For example, the questions “What are your office hours?” and “What time do you open?” are grouped together.

## Detailed Calls Tab

The **Detailed Calls** tab provides a comprehensive table of all analyzed calls with sortable columns and detailed metrics for each call.

<Frame>
  <img alt="Detailed calls table with sortable columns" />
</Frame>

### Calls Table

The table displays the following information for each call:

* Call ID
* Eval
* Call Start Time
* Call Length
* LLM Hallucination Rate
* KB Recall
* Transition Accuracy
* User Positive Sentiment Rate
* Latency P50
* Overlapping Speech Count
* WER
* Tool Call Accuracy
* Natural Tonality Rate

### Sorting and Filtering

* **Sort columns**: Click any column header to sort by that metric
* **Filter calls**: Use the Filter button to apply date ranges, score thresholds, etc

<Info>
  Use the ellipsis menu (⋯) in the Action column to:

  * Rerun QA for a call
  * Delete a call from QA
</Info>

## Call-Level QA Sheet

Clicking on any row in the Detailed Calls table opens a **Call QA Sheet** that provides comprehensive diagnostics for that specific call.

### QA Result Overview

The QA sheet displays:

* **Overall Score**: Pass/Fail status with numerical score
* **Passed Metrics**: Metrics that met the defined thresholds (shown with green checkmarks)
* **Failed Metrics**: Metrics that didn't meet thresholds (shown with orange warning triangles)

<Frame>
  <img alt="Call QA sheet with metrics and recommendations" />
</Frame>

### Calibrate Call QA

You can calibrate individual call QA results by manually adjusting metric evaluations:

* **Mark passed metrics as failed**: Override automatic evaluation if a metric should have failed
* **Mark failed metrics as passed**: Override automatic evaluation if a metric should have passed

You can also add custom notes to any call QA.

### Transcript and Errors

The QA sheet provides access to:

* **Full call transcript**: Complete conversation between user and agent
* **Transcript errors**: Specific transcription mistakes with corrections
* **Error highlights**: Visual indicators showing where errors occurred

<Frame>
  <img alt="Transcript errors with corrections" />
</Frame>

<Warning>
  Low scores or high failure rates may indicate systemic issues with your agent configuration, prompts, or knowledge base. Review multiple failed calls to identify patterns before making changes.
</Warning>


# Add Knowledge Base Sources
Source: https://docs.retellai.com/api-references/add-knowledge-base-sources

openapi-final post /add-knowledge-base-sources/{knowledge_base_id}
Add sources to a knowledge base

<RequestExample>
  ```javascript Javascript theme={null}
  import Retell from 'retell-sdk';
  import fs from 'fs';

  const client = new Retell({
    apiKey: 'YOUR_RETELL_API_KEY',
  });

  async function main() {
    const knowledgeBaseResponse = await client.knowledgeBase.addSources(
      "knowledge_base_xxxxxxxxxxxx",
      {
        knowledge_base_texts: [
          {
            title: "Sample Question",
            text: "Hello, how are you?",
          },
        ],
        knowledge_base_urls: [
          "https://www.retellai.com",
          "https://docs.retellai.com",
        ],
        knowledge_base_files: [
          fs.createReadStream("./sample.txt"),
        ],
      }
    );

    console.log(knowledgeBaseResponse.knowledge_base_id);
  }

  main();
  ```

  ```Python Python theme={null}
  from retell import Retell

  client = Retell(
      api_key="YOUR_RETELL_API_KEY",
  )

  file = open("./sample.txt", "rb")
  knowledge_base_response = client.knowledge_base.add_sources(
      knowledge_base_id="knowledge_base_xxxxxxxxxxxx",
      knowledge_base_texts=[
          {
              "title": "Sample Question",
              "text": "Hello, how are you?",
          },
      ],
      knowledge_base_urls=[
          "https://www.retellai.com",
          "https://docs.retellai.com",
      ],
      knowledge_base_files=[file],
  )
  print(knowledge_base_response.knowledge_base_id)
  file.close()
  ```

  ```bash cURL theme={null}
  curl --request POST \
    --url https://api.retellai.com/add-knowledge-base-sources/knowledge_base_xxxxxxxxxxxx \
    --header 'Authorization: Bearer YOUR_RETELL_API_KEY' \
    --form 'knowledge_base_texts=[{"title": "Sample Question", "text": "Hello, how are you?"}]' \
    --form 'knowledge_base_urls=["https://www.retellai.com", "https://docs.retellai.com"]' \
    --form 'knowledge_base_files=@./sample.txt'
  ```
</RequestExample>


# Add Voice
Source: https://docs.retellai.com/api-references/add-voice

openapi-final post /add-community-voice
Add a community voice to the voice library



# Agent Playground Completion
Source: https://docs.retellai.com/api-references/agent-playground-completion

openapi-final post /agent-playground-completion/{agent_id}
Stateless playground completion. Send the full conversation history (same shape as chat completion messages) and receive only the newly generated messages. Nothing is persisted server-side — the caller manages conversation state.



# Clone Voice
Source: https://docs.retellai.com/api-references/clone-voice

openapi-final post /clone-voice
Clone a voice from audio files



# Create Voice Agent
Source: https://docs.retellai.com/api-references/create-agent

openapi-final post /create-agent
Create a new agent



# Create Draft Agent Version
Source: https://docs.retellai.com/api-references/create-agent-version

openapi-final post /create-agent-version/{agent_id}
Create a new draft agent version from a base version.



# Create Batch Call
Source: https://docs.retellai.com/api-references/create-batch-call

openapi-final post /create-batch-call
Create a batch call



# Create Batch Test
Source: https://docs.retellai.com/api-references/create-batch-test

openapi-final post /create-batch-test
Create a batch test to run multiple test cases



# Create Chat
Source: https://docs.retellai.com/api-references/create-chat

openapi-final post /create-chat
Create a chat session



# Create Chat Agent
Source: https://docs.retellai.com/api-references/create-chat-agent

openapi-final post /create-chat-agent
Create a new chat agent



# Create Draft Chat Agent Version
Source: https://docs.retellai.com/api-references/create-chat-agent-version

openapi-final post /create-agent-version/{agent_id}
Create a new draft agent version from a base version.



# Create Chat Completion
Source: https://docs.retellai.com/api-references/create-chat-completion

openapi-final post /create-chat-completion
Create a chat completion message



# Create Conversation Flow
Source: https://docs.retellai.com/api-references/create-conversation-flow

openapi-final post /create-conversation-flow
Create a new Conversation Flow that can be attached to an agent. This is used to generate response output for the agent.



# Create Conversation Flow Component
Source: https://docs.retellai.com/api-references/create-conversation-flow-component

openapi-final post /create-conversation-flow-component
Create a new shared conversation flow component



# Create Knowledge Base
Source: https://docs.retellai.com/api-references/create-knowledge-base

openapi-final post /create-knowledge-base
Create a new knowledge base

<RequestExample>
  ```javascript Javascript theme={null}
  import Retell from 'retell-sdk';

  const client = new Retell({
    apiKey: 'YOUR_RETELL_API_KEY',
  });

  async function main() {
    const knowledgeBaseResponse = await client.knowledgeBase.create({
      knowledge_base_name: "Sample KB",
      knowledge_base_texts: [
        {
          text: "Hello, how are you?",
          title: "Sample Question",
        },
      ],
      knowledge_base_urls: [
        "https://www.retellai.com",
        "https://docs.retellai.com",
      ],
      knowledge_base_files: [
        fs.createReadStream("../sample.txt"),
      ],
    });

    console.log(knowledgeBaseResponse.knowledge_base_id);
  }

  main();
  ```

  ```Python Python theme={null}
  from retell import Retell

  client = Retell(
      api_key="YOUR_RETELL_API_KEY",
  )

  file = open("./test_data.txt", "rb")
  knowledge_base_response = client.knowledge_base.create(
      knowledge_base_name="Sample KB",
      knowledge_base_texts=[
          {
              "text": "Hello, how are you?",
              "title": "Sample Question",
          },
      ],
      knowledge_base_urls=[
        "https://www.retellai.com",
        "https://docs.retellai.com",
      ],
      knowledge_base_files=[file],
  )
  print(knowledge_base_response.knowledge_base_id)
  file.close()
  ```

  ```bash cURL theme={null}
  curl --request POST \
    --url https://api.retellai.com/create-knowledge-base \
    --header 'Authorization: Bearer <token>' \
    --form 'knowledge_base_name=Sample KB' \
    --form 'knowledge_base_texts=[{"title": "Sample Question", "text": "Hello, how are you?"}]' \
    --form 'knowledge_base_urls=["https://www.retellai.com", "https://docs.retellai.com"]' \
    --form 'knowledge_base_files=@./test_data.txt'
  ```
</RequestExample>


# Create Phone Call
Source: https://docs.retellai.com/api-references/create-phone-call

openapi-final post /v2/create-phone-call
Create a new outbound phone call



# Create Phone Number
Source: https://docs.retellai.com/api-references/create-phone-number

openapi-final post /create-phone-number
Buy a new phone number & Bind agents



# Create Retell LLM
Source: https://docs.retellai.com/api-references/create-retell-llm

openapi-final post /create-retell-llm
Create a new Retell LLM Response Engine that can be attached to an agent. This is used to generate response output for the agent.



# Create Outbound SMS
Source: https://docs.retellai.com/api-references/create-sms-chat

openapi-final post /create-sms-chat
Start an SMS chat session with a chat agent; MMS is understood by the agent when received.



# Create Test Case Definition
Source: https://docs.retellai.com/api-references/create-test-case-definition

openapi-final post /create-test-case-definition
Create a new test case definition



# Create Web Call
Source: https://docs.retellai.com/api-references/create-web-call

openapi-final post /v2/create-web-call
Create a new web call



# Delete Agent
Source: https://docs.retellai.com/api-references/delete-agent

openapi-final delete /delete-agent/{agent_id}
Delete an existing agent



# Delete Agent Version
Source: https://docs.retellai.com/api-references/delete-agent-version

openapi-final delete /delete-agent-version/{agent_id}
Delete a specific agent version.



# Delete Call
Source: https://docs.retellai.com/api-references/delete-call

openapi-final delete /v2/delete-call/{call_id}
Delete a specific call and its associated data



# Delete Chat
Source: https://docs.retellai.com/api-references/delete-chat

openapi-final delete /delete-chat/{chat_id}
Delete an existing chat



# Delete Chat Agent
Source: https://docs.retellai.com/api-references/delete-chat-agent

openapi-final delete /delete-chat-agent/{agent_id}
Delete an existing chat agent



# Delete Chat Agent Version
Source: https://docs.retellai.com/api-references/delete-chat-agent-version

openapi-final delete /delete-agent-version/{agent_id}
Delete a specific agent version.



# Delete Conversation Flow
Source: https://docs.retellai.com/api-references/delete-conversation-flow

openapi-final delete /delete-conversation-flow/{conversation_flow_id}
Delete a conversation flow and all its versions



# Delete Conversation Flow Component
Source: https://docs.retellai.com/api-references/delete-conversation-flow-component

openapi-final delete /delete-conversation-flow-component/{conversation_flow_component_id}
Delete a shared conversation flow component. When deleting a shared component, creates local copies for all linked conversation flows.



# Delete Knowledge Base
Source: https://docs.retellai.com/api-references/delete-knowledge-base

openapi-final delete /delete-knowledge-base/{knowledge_base_id}
Delete an existing knowledge base



# Delete Knowledge Base Source
Source: https://docs.retellai.com/api-references/delete-knowledge-base-source

openapi-final delete /delete-knowledge-base-source/{knowledge_base_id}/source/{source_id}
Delete an existing source from knowledge base



# Delete Phone Number
Source: https://docs.retellai.com/api-references/delete-phone-number

openapi-final delete /delete-phone-number/{phone_number}
Delete an existing phone number



# Delete Retell LLM
Source: https://docs.retellai.com/api-references/delete-retell-llm

openapi-final delete /delete-retell-llm/{llm_id}
Delete an existing Retell LLM Response Engine



# Delete Test Case Definition
Source: https://docs.retellai.com/api-references/delete-test-case-definition

openapi-final delete /delete-test-case-definition/{test_case_definition_id}
Delete a test case definition



# End Chat
Source: https://docs.retellai.com/api-references/end-chat

openapi-final patch /end-chat/{chat_id}
End an ongoing chat



# Get Voice Agent
Source: https://docs.retellai.com/api-references/get-agent

openapi-final get /get-agent/{agent_id}
Retrieve details of a specific agent



# Get Agent Versions
Source: https://docs.retellai.com/api-references/get-agent-versions

openapi-final get /get-agent-versions/{agent_id}
Get all versions of an agent



# Get Batch Test
Source: https://docs.retellai.com/api-references/get-batch-test

openapi-final get /get-batch-test/{test_case_batch_job_id}
Get a batch test job by ID



# Get Call
Source: https://docs.retellai.com/api-references/get-call

openapi-final get /v2/get-call/{call_id}
Retrieve details of a specific call



# Get Chat
Source: https://docs.retellai.com/api-references/get-chat

openapi-final get /get-chat/{chat_id}
Retrieve details of a specific chat



# Get Chat Agent
Source: https://docs.retellai.com/api-references/get-chat-agent

openapi-final get /get-chat-agent/{agent_id}
Retrieve details of a specific chat agent



# Get Chat Agent Versions
Source: https://docs.retellai.com/api-references/get-chat-agent-versions

openapi-final get /get-chat-agent-versions/{agent_id}
Get all versions of a chat agent



# Get Concurrency
Source: https://docs.retellai.com/api-references/get-concurrency

openapi-final get /get-concurrency
Get the current concurrency and concurrency limit of the org



# Get Conversation Flow
Source: https://docs.retellai.com/api-references/get-conversation-flow

openapi-final get /get-conversation-flow/{conversation_flow_id}
Retrieve details of a specific Conversation Flow



# Get Conversation Flow Component
Source: https://docs.retellai.com/api-references/get-conversation-flow-component

openapi-final get /get-conversation-flow-component/{conversation_flow_component_id}
Get a shared conversation flow component



# Get Knowledge Base
Source: https://docs.retellai.com/api-references/get-knowledge-base

openapi-final get /get-knowledge-base/{knowledge_base_id}
Retrieve details of a specific knowledge base



# Get MCP Tools
Source: https://docs.retellai.com/api-references/get-mcp-tools

openapi-final get /get-mcp-tools/{agent_id}
Get MCP tools for a specific agent



# Get Phone Number
Source: https://docs.retellai.com/api-references/get-phone-number

openapi-final get /get-phone-number/{phone_number}
Retrieve details of a specific phone number



# Get Retell LLM
Source: https://docs.retellai.com/api-references/get-retell-llm

openapi-final get /get-retell-llm/{llm_id}
Retrieve details of a specific Retell LLM Response Engine



# Get Test Case Definition
Source: https://docs.retellai.com/api-references/get-test-case-definition

openapi-final get /get-test-case-definition/{test_case_definition_id}
Get a test case definition by ID



# Get Test Run
Source: https://docs.retellai.com/api-references/get-test-run

openapi-final get /get-test-run/{test_case_job_id}
Get a test case job (test run) by ID



# Get Voice
Source: https://docs.retellai.com/api-references/get-voice

openapi-final get /get-voice/{voice_id}
Retrieve details of a specific voice



# Import Phone Number
Source: https://docs.retellai.com/api-references/import-phone-number

openapi-final post /import-phone-number
Import a phone number from custom telephony & Bind agents



# List Voice Agents
Source: https://docs.retellai.com/api-references/list-agents

openapi-final get /list-agents
List all agents



# List Batch Tests
Source: https://docs.retellai.com/api-references/list-batch-tests

openapi-final get /v2/list-batch-tests
List batch test jobs with pagination



# List Calls
Source: https://docs.retellai.com/api-references/list-calls

openapi-final post /v3/list-calls
List calls with unified cursor pagination response.



# List Chat Agents
Source: https://docs.retellai.com/api-references/list-chat-agents

openapi-final get /list-chat-agents
List all chat agents



# List Chats
Source: https://docs.retellai.com/api-references/list-chats

openapi-final post /v3/list-chats
List chats with unified cursor pagination response.



# List Conversation Flow Components
Source: https://docs.retellai.com/api-references/list-conversation-flow-components

openapi-final get /v2/list-conversation-flow-components
List shared conversation flow components with pagination



# List Conversation Flows
Source: https://docs.retellai.com/api-references/list-conversation-flows

openapi-final get /v2/list-conversation-flows
List conversation flows with pagination



# List Export Requests
Source: https://docs.retellai.com/api-references/list-export-requests

openapi-final get /v2/list-export-requests
List export requests with pagination



# List Knowledge Bases
Source: https://docs.retellai.com/api-references/list-knowledge-bases

openapi-final get /list-knowledge-bases
List all knowledge bases



# List Phone Numbers
Source: https://docs.retellai.com/api-references/list-phone-numbers

openapi-final get /v2/list-phone-numbers
List phone numbers with pagination



# List Retell LLMs
Source: https://docs.retellai.com/api-references/list-retell-llms

openapi-final get /v2/list-retell-llms
List Retell LLM Response Engines with pagination



# List Test Case Definitions
Source: https://docs.retellai.com/api-references/list-test-case-definitions

openapi-final get /v2/list-test-case-definitions
List test case definitions with pagination



# List Test Runs
Source: https://docs.retellai.com/api-references/list-test-runs

openapi-final get /v2/list-test-runs/{test_case_batch_job_id}
List test case jobs (test runs) for a batch test job with pagination



# List Voices
Source: https://docs.retellai.com/api-references/list-voices

openapi-final get /list-voices
List all voices available to the user



# LLM WebSocket
Source: https://docs.retellai.com/api-references/llm-websocket

Retell AI connects with your server, and get responses / actions from your custom LLM.

<Warning>
  Retell agent frameworks like single prompt, conversation flow provides more capabilities and built in tool sets. We recommend using those frameworks if possible. Only use custom LLM integration if you have to due to specific compliance or use case requirements.
</Warning>

<Note>Please follow the [Custom LLM Integration Guide](/integrate-llm/overview) for step by step instructions on how to integrate your custom LLM. This doc is to show the underlying protocols
of what our server would send to yours, and what we expect to receive. </Note>

## Overview

This socket shall connect directly to your server, where you would get live transcript and
other relevant inputs from us, and provide responses back to us using your custom LLM.
In short, this WebSocket controls what the agents says, and controls actions like ending the call.

Retell AI will initiate this WebSocket when starting the call,
and your server should get prepared to handle it.

## Endpoint

<Note>WebSocket Endpoint: `{your-server-websocket-endpoint}/{call_id}`</Note>

### Path Parameters

<ParamField type="string">
  Unique call id to identify the call.
</ParamField>

## Protocol

Retell and your server would conform to the following protocol sending the WebSocket messages to communicate.

All message event type is "text", where the `data` attribute of message event is
a JSON object stringified.

### Event Flow

The connection would start by your server sends an optional [config event](/api-references/llm-websocket#config-event) to Retell,
and a [response event](/api-references/llm-websocket#response-event)
that serves as the begin message for agent to speak.
Set content to empty string if you want the agent to wait for user to start the conversation.

Retell would send back a [call details event](/api-references/llm-websocket#call-details-event) if that's enabled in config.
Retell and your server would periodically send [ping pong events](/api-references/llm-websocket#ping-pong-event)
to keep the connection alive if configured in config.

As the call goes, Retell would send over live transcript and other updates in
[update only events](/api-references/llm-websocket#update-only-event), and determine when is appropriate to
ask for responses / reminders in
[response and reminder required events](/api-references/llm-websocket#response-and-reminder-required-events). Your server will be
sending back [response events](/api-references/llm-websocket#response-event) accordingly.
Not all your responses would get spoken out, cause the user might
continue to speak even when Retell thought it would be agent's turn.

If at certain point, you want agent to jump in the conversation and speak something immediately, you can send an
[agent interrupt event](/api-references/llm-websocket#agent-interrupt-event).

### Retell -> Your Server Event Spec

There will be a couple events that Retell can send to your server in this websocket,
to differentiate between them, check the `interaction_type` field:

* `ping_pong`: (optional) to check for disconnection and keep the connection alive
* `update_only`: (required) to send real time updates about the call like live transcript
* `response_required`: (required) ask for response content from your server
* `reminder_required`: (required) ask for reminder content from your server

#### Ping Pong Event

When you set `auto_reconnect` to true in the [config event](/api-references/llm-websocket#config-event),
Retell will send ping\_pong events to your server
every 2s to keep the connection alive.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `ping_pong`
</ParamField>

<ParamField type="integer">
  Timestamp (milliseconds since epoch) of when Retell send this event.
  You can use this to calculate the time taken for the round trip.
</ParamField>

#### Call Details Event

When you set `call_details` to true in the [config event](/api-references/llm-websocket#config-event),
Retell will send call details events to your server right away so that you can save the time of retrieving call detail from
[Get Call API](/api-references/get-call).

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `call_details`
</ParamField>

<ParamField type="object">
  Contains the response from [Register Call API](/api-references/register-call).
</ParamField>

#### Update Only Event

Retell would send event when transcript updates -- either user speaks, or agent speaks.
Retell also sends this event when turntaking happens.

<ParamField type="enum<string>">
  Event type. This event is simply a update containing the latest transcript or turntaking information, no response required.

  Available options: `update_only`
</ParamField>

<ParamField type="object[]">
  Complete live transcript collected in the call so far. Presented in the form of a list of
  utterances.

  See `transcript_object` field of [Get Call API Response](/api-references/get-call) for the detailed schema
  for the object in the list.
</ParamField>

<ParamField type="object[]">
  Transcript of the call weaved with tool call invocation and results. Populated when `transcript_with_tool_calls` field is set to
  true in the [config event](/api-references/llm-websocket#config-event).

  It precisely captures when (at what utterance, which word) the tool was invoked and what was the result
  if the tool calls were sent timely in this LLM websocket. See
  [tool call invocation event](/api-references/llm-websocket#tool-call-invocation-event)
  and [tool call result event](/api-references/llm-websocket#tool-call-result-event) for more information of how to send
  tool call invocations and results.

  See `transcript_with_tool_calls` field of [Get Call API Response](/api-references/get-call) for the detailed schema
  for the object in the list.
</ParamField>

<ParamField type="enum<string>">
  Indicates change of speaker (turn taking). This field will be present when speaker changes to user (user turn), or right before
  agent is about to speak (agent turn). This field can be helpful determining when to call functions in the call.

  Available options: `agent_turn`, `user_turn`
</ParamField>

#### Response and Reminder Required Events

Retell would continuously assess if it's a good time for agent to speak, and would
ask for content for response / reminder when appropriate, but not all
responses Retell ask for would get spoken out (as user might continue to speak).

<ParamField type="enum<string>">
  Determines what do we need from your server.

  * `response_required`: Require a response from your server for the current live transcript.
  * `reminder_required`: User has not spoken for a while, a reminder is needed from your server.

  Available options: `response_required`, `reminder_required`
</ParamField>

<ParamField type="integer">
  This unique auto incrementing id is used to track the response Retell needs, and used to identify the
  responses streamed from your server, as you can
  send multiple events to stream back responses, and we need an id to group them.

  When a new response is needed, a new event with response id will
  be sent, and all previous responses will be discarded.
</ParamField>

<ParamField type="object[]">
  Complete live transcript collected in the call so far. Presented in the form of a list of
  utterances.

  See `transcript_object` field of [Get Call API Response](/api-references/get-call) for the detailed schema
  for the object in the list.
</ParamField>

<ParamField type="object[]">
  Transcript of the call weaved with tool call invocation and results. Populated when `transcript_with_tool_calls` field is set to
  true in the [config event](/api-references/llm-websocket#config-event).

  It precisely captures when (at what utterance, which word) the tool was invoked and what was the result
  if the tool calls were sent timely in this LLM websocket. See
  [tool call invocation event](/api-references/llm-websocket#tool-call-invocation-event)
  and [tool call result event](/api-references/llm-websocket#tool-call-result-event) for more information of how to send
  tool call invocations and results.

  See `transcript_with_tool_calls` field of [Get Call API Response](/api-references/get-call) for the detailed schema
  for the object in the list.
</ParamField>

### Your Server -> Retell Event Spec

There will be a couple events that your server can send to Retell in this websocket,
to differentiate between them, set the `response_type` field:

* `config`: (optional) the initial config for configuring reconnection, whether to send call details etc
* `ping_pong`: (optional) to check for disconnection and keep the connection alive
* `response`: (required) to send back responses to the user when requested
* `agent_interrupt`: (optional) to jump in conversation and speak content in it immediately, interrupts both
  agent and user.
* `tool_call_invocation`: (optional) to bookkeep and weave tool call invocations and results in the transcript.
* `tool_call_result`: (optional) to bookkeep and weave tool call invocations and results in the transcript.
* `metadata`: (optional) to pass some data from the server where the LLM is running to the frontend during a web call.

#### Config Event

You can send a config at connection open to configure reconnection, whether to send call details etc.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `config`
</ParamField>

<ParamField type="object">
  Configuration object to control whether to auto reconnect, and whether Retell sends a call detail over.

  <Expandable title="properties">
    <ResponseField name="auto_reconnect" type="boolean">
      If set to true, Retell will send ping pong events to your server, and would expect ping pong events back
      from your server every 2s. Once there's 5s without ping pong event, Retell would close the current connection
      and restart a new connection to your server for up to 2 times.
    </ResponseField>

    <ResponseField name="call_details" type="boolean">
      If set to true, Retell will send call details over to your server right away. See
      [call details event](/api-references/llm-websocket#call-details-event) for more information.
    </ResponseField>

    <ResponseField name="transcript_with_tool_calls" type="boolean">
      If set to true, Retell will populate an additional field in the [update only events](/api-references/llm-websocket#update-only-event),
      [response and reminder required events](/api-references/llm-websocket#response-and-reminder-required-events).
      This additional field will contain
      transcript of the call weaved with tool call invocation and results.

      You need to send tool call invocations and results to us in websocket so that we can construct it. See
      [tool call invocation event](/api-references/llm-websocket#tool-call-invocation-event)
      and [tool call result event](/api-references/llm-websocket#tool-call-result-event) for more information of how to send
      tool call invocations and results.
    </ResponseField>
  </Expandable>
</ParamField>

#### Update Agent Event

You can send agent update events at any time of the call to update some of the agent configurations.
We might add more configuration to this event in the future.

This can be useful when you want to modify the agent behavior during the call, like when
you want to use reminders as a way to let agent continue speaking, or you wish to make agent
less responsive when user is looking up information.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `update_agent`
</ParamField>

<ParamField type="object">
  Set what agent configuration you want to update. All fields are optional.

  <Expandable title="properties">
    <ResponseField name="responsiveness" type="number">
      Controls how responsive is the agent. Value ranging from \[0,1].
      Lower value means less responsive agent (wait more, respond slower),
      while higher value means faster exchanges (respond when it can).
    </ResponseField>

    <ResponseField name="interruption_sensitivity" type="number">
      Controls how sensitive the agent is to user interruptions. Value
      ranging from \[0,1]. Lower value means it will take longer / more
      words for user to interrupt agent, while higher value means it's
      easier for user to interrupt agent.
    </ResponseField>

    <ResponseField name="reminder_trigger_ms" type="number">
      If set (in milliseconds), will trigger a reminder to the agent to
      speak if the user has been silent for the specified duration after
      some agent speech. Must be a positive number.
    </ResponseField>

    <ResponseField name="reminder_max_count" type="number">
      If set, controls how many times agent would remind user when user is
      unresponsive. Must be a non negative integer. Set to 0 to disable agent from
      reminding.
    </ResponseField>
  </Expandable>
</ParamField>

#### Ping Pong Event

When you set `auto_reconnect` to true in the [config event](/api-references/llm-websocket#config-event),
you need to send ping\_pong events to signal that your server
is still alive. Retell would expect a ping\_pong event back every 2s, and would close the connection if there's no ping\_pong
event for 5s.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `ping_pong`
</ParamField>

<ParamField type="integer">
  Timestamp (milliseconds since epoch) of when your server send this event.
  Retell would use this to calculate the time taken for the round trip.
</ParamField>

#### Response Event

Your server needs to respond to [response and reminder required events](/api-references/llm-websocket#response-and-reminder-required-events)
so that agent can speak in time.
You can stream the response or send it in one go, although streaming is
recommended for lower latency. When a newer event that require response / reminder is received, you can
stop responding to the previous response / reminder required events, as it would not get used. You still need to respond to
previous response / reminder required event if newer update\_only events are received.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `response`
</ParamField>

<ParamField type="integer">
  Indicates which requested response this is answering.
</ParamField>

<ParamField type="string">
  Partial or full content response content.
</ParamField>

<ParamField type="boolean">
  Whether the content is complete. When streaming responses back, only the last event of the response
  should have this field set to true.
</ParamField>

<ParamField type="boolean">
  If set to true, agent would not get interrupted by user for content in this event. Useful for conveying important information.
</ParamField>

<ParamField type="boolean">
  If set to true, Retell would end the call after content associated with this id is fully spoken. If agent was interrupted
  during speaking, the end call signal would get discarded.
</ParamField>

<ParamField type="string">
  If set, Retell would transfer the call to the number specified here after content associated with this id is fully spoken.
  Only applicable to Retell numbers or imported numbers.  If your voice agent is using custom telephony via the dial to
  SIP endpoint route, you need to write your own call transfer logic.
</ParamField>

<ParamField type="boolean">
  If set to true, the transferee will see the original caller's number instead of the Retell number when the call is transferred.
</ParamField>

<ParamField type="string">
  If set, Retell would press the input digit or digits to send DTMF tones after content associated with this id is fully spoken
  (although you probably do not want the voice agent to speak anything when pressing digits).
</ParamField>

#### Agent Interrupt Event

If at certain point, you want to jump in the conversation and speak something immediately, you can send this event.
It will stop the agent speech if the agent is speaking, or it will interrupt the user if the user is speaking.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `agent_interrupt`
</ParamField>

<ParamField type="integer">
  Used to group the interrupt events. This is a unique id maintained in your server. If interrupt events with same
  ids are received, the content would get spoken in order of the interrupt events received. If interrupt events with
  different ids are received, the previous interrupt events are discarded.
</ParamField>

<ParamField type="string">
  Partial or full content response content.
</ParamField>

<ParamField type="boolean">
  Whether the content is complete. When streaming responses back, only the last event of the response
  should have this field set to true.
</ParamField>

<ParamField type="boolean">
  If set to true, agent would not get interrupted by user for content in this event.
  This is recommended to set to true here because without this setting,
  if user is talking, and agent interrupts here, the two party would
  speak at the same time, and agent would get interrupted quickly.
</ParamField>

<ParamField type="boolean">
  If set to true, and if this response is used for agent to speak,
  we would end the call after content is fully spoken.
</ParamField>

<ParamField type="string">
  If set, we will transfer the call to the number specified here after content is fully spoken.
  Only applicable to numbers purchased through Retell.
  For call transfer with your own Twilio account, you can trigger it from your server directly.
</ParamField>

<ParamField type="string">
  If set, Retell would press the input digit or digits to send DTMF tones after content associated with this id is fully spoken
  (although you probably do not want the voice agent to speak anything when pressing digits).
</ParamField>

#### Tool Call Invocation Event

If you send the tool call invocation and results in the websocket,
Retell would populate the `transcript_with_tool_calls` field in the [Get Call API Response](/api-references/get-call)
after call ends. We would weave the transcript and precisely capture when (at what utterance, which word)
the tool was invoked and what was the result.

If you also set `transcript_with_tool_calls` to true in the [config event](/api-references/llm-websocket#config-event),
Retell would populate the `transcript_with_tool_calls`
field in the [update only event](/api-references/llm-websocket#update-only-event) with the tool call invocations and results.
This is helpful when you do not wish to maintain a copy of transcript and function calls locally during the call session
and wish to have Retell manages it for you.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `tool_call_invocation`
</ParamField>

<ParamField type="string">
  Tool call id, globally unique.
</ParamField>

<ParamField type="string">
  Name of the function in this tool call.
</ParamField>

<ParamField type="string">
  Arguments for this tool call, it's a stringified JSON object.
</ParamField>

#### Tool Call Result Event

If you send the tool call invocation and results in the websocket,
Retell would populate the `transcript_with_tool_calls` field in the [Get Call API Response](/api-references/get-call)
after call ends. We would weave the transcript and precisely capture when (at what utterance, which word)
the tool was invoked and what was the result.

If you also set `transcript_with_tool_calls` to true in the [config event](/api-references/llm-websocket#config-event),
Retell would populate the `transcript_with_tool_calls`
field in the [update only event](/api-references/llm-websocket#update-only-event) with the tool call invocations and results.
This is helpful when you do not wish to maintain a copy of transcript and function calls locally during the call session
and wish to have Retell manages it for you.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `tool_call_result`
</ParamField>

<ParamField type="string">
  Tool call id, globally unique.
</ParamField>

<ParamField type="string">
  Result of the tool call, can be a string, a stringified json, etc.
</ParamField>

#### Metadata Event

Sometimes you may wish to pass some data from the server where the LLM is running to the frontend during a web call,
for animation purposes or other stuff. It can be challenging to make sure the frontend of the call is connecting from
can connect to the server where the LLM is running. In this case, you can send metadata events to the Retell and Retell will
forward it to the frontend.

See [frontend metadata event](/api-references/audio-websocket#metadata-event) for the forwarded event.

<ParamField type="enum<string>">
  Differentiate what this event is.

  Available options: `metadata`
</ParamField>

<ParamField type="object">
  You can put anything here that can be json serialized.
</ParamField>

## Sample Events

### Retell -> Your Server Sample Events

<CodeGroup>
  ```json Ping Pong theme={null}
  {
    "interaction_type": "ping_pong",
    "timestamp": 1703302407333
  }
  ```

  ```json Call Details theme={null}
  {
    "interaction_type": "call_details",
    "call": {
      "call_type": "phone_call",
      "from_number": "+12137771234",
      "to_number": "+12137771235",
      "direction": "inbound",
      "call_id": "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6",
      "agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
      "call_status": "registered",
      "metadata": {},
      "retell_llm_dynamic_variables": {
        "customer_name": "John Doe"
      },
      "opt_out_sensitive_data_storage": true
    }
  }
  ```

  ```json Response Required theme={null}
  {
    "interaction_type": "response_required",
    "timestamp": 3,
    "transcript": [
      {
        "role": "agent",
        "content": "Hey how can I help you?",
        "words": [Array]
      },
      {
        "role": "user",
        "content": "Hey. How are you?",
        "words": [Array]
      }
    ]
  }
  ```

  ```json Update Only theme={null}
  {
    "interaction_type": "update_only",
    "transcript": [
      {
        "role": "agent",
        "content": "Hey how can I help you?"
        "words": [Array]
      },
      {
        "role": "user",
        "content": "Hey. How are you?",
        "words": [
          {
            "word": "Hey.",
            "start": 4.375,
            "end": 4.615
          },
          {
            "word": "How",
            "start": 4.615,
            "end": 4.855
          },
          {
            "word": "are",
            "start": 4.855,
            "end": 5.030156
          },
          {
            "word": "you?",
            "start": 5.030156,
            "end": 5.2053127
          }
        ]
      }
    ],
    "turntaking": "agent_turn"
  }
  ```

  ```json Reminder Required theme={null}
  {
    "interaction_type": "reminder_required",
    "transcript": [
      {
        "role": "agent",
        "content": "Hey how can I help you?",
        "words": [Array]
      },
      {
        "role": "user",
        "content": "Hey. How are you?",
        "words": [Array]
      },
      {
        "role": "agent",
        "content": "I'm doing fine. How can I help you?",
        "words": [Array]
      }
    ]
  }
  ```
</CodeGroup>

### Your Server -> Retell Sample Events

<CodeGroup>
  ```json Config theme={null}
  {
    "response_type": "config",
    "config": {
      "auto_reconnect": true,
      "call_details": true
    }
  }
  ```

  ```json Agent Update theme={null}
  {
    "response_type": "update_agent",
    "agent_config": {
      "responsiveness": 0.5,
      "interruption_sensitivity": 0.5,
      "reminder_trigger_ms": 5000,
      "reminder_max_count": 3
    }
  }
  ```

  ```json Ping Pong theme={null}
  {
    "response_type": "ping_pong",
    "timestamp": 1703302407333
  }
  ```

  ```json Response theme={null}
  {
    "response_type": "response",
    "response_id": 3,
    "content": "I'm doing great, ",
    "content_complete": false
  }

  {
    "response_type": "response",
    "response_id": 3,
    "content": "thank you.",
    "content_complete": true
  }

  // Later on, ending the call
  {
    "response_type": "response",
    "response_id": 10,
    "content": "Goodbye.",
    "content_complete": true,
    "end_call": true
  }
  ```

  ```json Agent Interrupt theme={null}
  {
    "response_type": "agent_interrupt",
    "interrupt_id": 1,
    "content": "Please stop right there, do not",
    "content_complete": false,
    "no_interruption_allowed": true
  }

  {
    "response_type": "agent_interrupt",
    "interrupt_id": 1,
    "content": " click on that button yet!",
    "content_complete": true,
    "no_interruption_allowed": true
  }
  ```

  ```json Tool Call Invocation theme={null}
  {
    "response_type": "tool_call_invocation",
    "tool_call_id": "some_id_here",
    "name": "book_appointment",
    "arguments": "{\"date\": \"2022-01-01\", \"time\": \"10:00\"}"
  }
  ```

  ```json Tool Call Result theme={null}
  {
    "response_type": "tool_call_result",
    "tool_call_id": "some_id_here",
    "content": "Appointment booked successfully."
  }
  ```

  ```json Metadata theme={null}
  {
    "response_type": "metadata",
    "metadata": {
      "avatar_emotion": "Angry",
      "user_id": "1234"
    }
  }
  ```
</CodeGroup>


# Publish Agent
Source: https://docs.retellai.com/api-references/publish-agent

openapi-final post /publish-agent-version/{agent_id}
Publish an existing draft version in place.



# Publish Chat Agent
Source: https://docs.retellai.com/api-references/publish-chat-agent

openapi-final post /publish-agent-version/{agent_id}
Publish an existing draft version in place.



# Register Phone Call
Source: https://docs.retellai.com/api-references/register-phone-call

openapi-final post /v2/register-phone-call
Register a phone call to obtain a call ID and SIP URI for dial-to-SIP flows. The timeout is 5 minutes.



# Search Voice
Source: https://docs.retellai.com/api-references/search-voice

openapi-final post /search-community-voice
Search for community voices from voice providers



# Stop Call
Source: https://docs.retellai.com/api-references/stop-call

openapi-final post /v2/stop-call/{call_id}
Stop an ongoing call.



# Update Voice Agent
Source: https://docs.retellai.com/api-references/update-agent

openapi-final patch /update-agent/{agent_id}
Update an existing agent's latest draft version



# Update Call
Source: https://docs.retellai.com/api-references/update-call

openapi-final patch /v2/update-call/{call_id}
Update metadata and sensitive data storage settings for an existing call.



# Update Chat
Source: https://docs.retellai.com/api-references/update-chat

openapi-final patch /update-chat/{chat_id}
Update metadata and sensitive data storage settings for an existing chat.



# Update Chat Agent
Source: https://docs.retellai.com/api-references/update-chat-agent

openapi-final patch /update-chat-agent/{agent_id}
Update an existing chat agent



# Update Conversation Flow
Source: https://docs.retellai.com/api-references/update-conversation-flow

openapi-final patch /update-conversation-flow/{conversation_flow_id}
Update an existing conversation flow



# Update Conversation Flow Component
Source: https://docs.retellai.com/api-references/update-conversation-flow-component

openapi-final patch /update-conversation-flow-component/{conversation_flow_component_id}
Update an existing shared conversation flow component



# Update Phone Number
Source: https://docs.retellai.com/api-references/update-phone-number

openapi-final patch /update-phone-number/{phone_number}
Update agent bound to a purchased phone number



# Update Retell LLM
Source: https://docs.retellai.com/api-references/update-retell-llm

openapi-final patch /update-retell-llm/{llm_id}
Update an existing Retell LLM Response Engine



# Update Test Case Definition
Source: https://docs.retellai.com/api-references/update-test-case-definition

openapi-final put /update-test-case-definition/{test_case_definition_id}
Update a test case definition



# Add pause or read slowly
Source: https://docs.retellai.com/build/add-pause

Control speech pacing by adding spaced dashes for pauses in agent responses.

Although you can adjust general speed of the audio by changing the voice speed, you might want to
slow down the agent's speech only at certain points (like reading phone numbers).
You can do this by prompting the LLM and generating text with `-` in between (note, the space around `-` is important):

```json theme={null}
The number is 2 - 1 - 3 - 4
```

<Warning>
  Note: The spaces around the dash (`-`) are important for proper pausing behavior.
</Warning>

### How to add long pauses

Sometimes you might want to add longer pauses to the conversation. You can do this by adding multiple `-` in between the words.

Important: The spaces around the dash (`-`) are important for proper pausing behavior:

```json theme={null}
The number is 2 -  -  -  - 1 -  -  -  - 3
// Notice the double spaces between the dashes
```


# Add custom pronunciation
Source: https://docs.retellai.com/build/add-pronunciation

Customize word pronunciation in Retell AI using IPA or CMU phonetic dictionaries for 11Labs voices

<Note> This feature only works with English agents using 11Labs voices that selected the `eleven turbo v2` (English only) voice model. </Note>

<Frame>
  <img alt="Pronunciation dictionary" />
</Frame>

You can also control how certain words are pronounced. This is useful when you want to make sure certain
uncommon words are pronounced correctly.

To use the feature, you simply set a pronunciation dictionary for the agent, which consists of:

* the word to be pronounced. For example, `actually`
* the phonetic alphabet to use, right now `ipa` and `cmu` are supported.
* the phonetic pronunciation of the word. For example, `æktʃuəli`

You can search online to find the phonetic pronunciation of a word, or use tools like:

* [IPA pronouncing dictionary tool](https://tophonetics.com/)
* [CMU pronouncing dictionary tool](http://www.speech.cs.cmu.edu/cgi-bin/cmudict/)


# Agent Handbook
Source: https://docs.retellai.com/build/agent-handbook

Enable pre-built best-practice prompts that improve agent personality, accuracy, and safety with a single toggle.

The Agent Handbook is a collection of ready-to-use prompt presets that improve how your agent communicates. Each preset encodes a specific best practice — toggle it on and the behavior is added automatically, no prompt writing needed.

<Note>New agents are created with **Default Personality** and **AI Disclosure When Asked** enabled by default.</Note>

## How It Works

The Agent Handbook organizes presets into three categories:

* **Personality & Tone** — Shape how the agent sounds and feels in conversation
* **Accuracy & Format** — Improve how the agent handles names, numbers, and data (voice agents only)
* **Trust & Safety** — Control transparency and scope of responses

Toggle any preset on or off from the Agent Handbook panel. Each preset adds a small number of tokens to every interaction — estimated token counts are shown on hover.

<Frame>
  <img alt="Agent Handbook button in agent settings" />
</Frame>

To open the Agent Handbook, click the **Agent Handbook** button in the prompt section of your agent settings.

<Frame>
  <img alt="Agent Handbook panel with preset toggles" />
</Frame>

## Presets

### Personality & Tone

<AccordionGroup>
  <Accordion title="Default Personality (~480 tokens)">
    **Available for:** Voice and Chat agents | **Default:** Enabled

    Makes your agent sound like a professional representative. It follows an **Acknowledge → Statement → Next Step** response structure, limits filler acknowledgments, avoids robotic phrases like "Certainly!" or "Absolutely!", and keeps responses concise and conversational.

    **When to use:** Leave enabled unless you have a highly custom personality defined in your own prompt.

    **Example:** *"I understand this is frustrating — let me look into that for you."*
  </Accordion>

  <Accordion title="Natural Filler Words (~100 tokens)">
    **Available for:** Voice agents only | **Default:** Disabled

    Adds occasional filler words like "um", "uh", and "you know" to make the agent sound more human and conversational. Fillers are used sparingly — roughly once every 2–3 sentences.

    **When to use:** Great for sales, customer success, or casual conversations. Avoid for formal or regulated contexts (medical, legal).

    **Example:** *"So yeah, let me just pull that up for you real quick."*
  </Accordion>

  <Accordion title="High Empathy (~70 tokens)">
    **Available for:** Voice and Chat agents | **Default:** Disabled

    Guides the agent to use empathetic language when the situation calls for it — acknowledging concerns, making callers feel heard, and reassuring them before moving to a solution.

    **When to use:** Useful for support agents, complaint handling, or any scenario where callers may be frustrated or emotional.

    **Example:** *"I'm sorry you're dealing with this. Let's get it sorted."*
  </Accordion>
</AccordionGroup>

### Accuracy & Format

<Note>All presets in this category are available for voice agents only. They are automatically disabled for chat agents.</Note>

<AccordionGroup>
  <Accordion title="Echo Verification (~190 tokens)">
    **Default:** Disabled

    The agent repeats back names, phone numbers, and other critical details for confirmation. For uncommon names, it spells them out letter by letter.

    **When to use:** Enable for appointment booking, data collection, or any workflow where accurate information capture is critical.

    **Example:** *"Just to confirm, your first name is Ryan, last name is James — is that correct?"*
  </Accordion>

  <Accordion title="NATO Phonetic Alphabet (~190 tokens)">
    **Default:** Disabled

    When spelling is needed, the agent uses the NATO phonetic alphabet (A as in Alfa, B as in Bravo, etc.) with natural pauses for clarity.

    **When to use:** Useful for confirming email addresses, reference numbers, account IDs, or names over the phone.

    **Example:** *"That's B as in Bravo, 7, K as in Kilo, 2 — correct?"*
  </Accordion>

  <Accordion title="Speech Normalization (~910 tokens)">
    **Default:** Disabled

    Formats numbers, dates, money, phone numbers, addresses, and emails into natural spoken form. For example, "\$758.08" becomes "seven fifty-eight dollars and eight cents" and phone numbers are read digit by digit with pauses.

    **When to use:** Enable when your agent frequently reads back structured data like prices, dates, or contact information. Note the higher token cost (\~910 tokens).

    <Tip>This preset tells the LLM how to format its text output for natural speech. For converting text to spoken form at the audio level, enable the `speech_normalization` option in `handbook_config`. Both can be used together.</Tip>

    **Example:** *"Your total is seventy dollars and eighty-four cents."*
  </Accordion>

  <Accordion title="Smart Matching (~110 tokens)">
    **Default:** Disabled

    Handles common speech recognition variations of names gracefully. If a caller confirms their name but the transcription is slightly different (e.g., "Brandon" vs. "Brendon"), the agent treats it as a match and continues naturally.

    **When to use:** Enable when your agent looks up names in a database or CRM and needs tolerance for transcription variations.

    **Example:** Agent asks "Are you Brandon?" and the caller says "Yes, this is Brendon" — the agent continues without flagging the difference.
  </Accordion>
</AccordionGroup>

### Trust & Safety

<AccordionGroup>
  <Accordion title="AI Disclosure When Asked (~30 tokens)">
    **Available for:** Voice and Chat agents | **Default:** Enabled

    When someone asks if they're speaking to a human or an AI, the agent clearly acknowledges that it's a virtual assistant.

    **When to use:** Recommended for transparency and compliance. Only disable if your use case has specific reasons not to disclose.

    **Example:** *"Yes — I'm an AI assistant here to help."*
  </Accordion>

  <Accordion title="Scope Boundaries (~60 tokens)">
    **Available for:** Voice and Chat agents | **Default:** Disabled

    Restricts the agent to only answer questions based on information available in its prompt and knowledge base. If it doesn't know, it says so instead of guessing.

    **When to use:** Enable for any agent where factual accuracy is critical, such as healthcare, finance, or legal use cases.

    **Example:** *"I don't have that information, but I can connect you to someone who can help."*
  </Accordion>
</AccordionGroup>

## Token Cost Summary

| Preset                   | Est. Tokens | Voice | Chat | Default |
| ------------------------ | ----------- | ----- | ---- | ------- |
| Default Personality      | \~480       | ✓     | ✓    | On      |
| Natural Filler Words     | \~100       | ✓     | —    | Off     |
| High Empathy             | \~70        | ✓     | ✓    | Off     |
| Echo Verification        | \~190       | ✓     | —    | Off     |
| NATO Phonetic Alphabet   | \~190       | ✓     | —    | Off     |
| Speech Normalization     | \~910       | ✓     | —    | Off     |
| Smart Matching           | \~110       | ✓     | —    | Off     |
| AI Disclosure When Asked | \~30        | ✓     | ✓    | On      |
| Scope Boundaries         | \~60        | ✓     | ✓    | Off     |

<Note>Token counts are approximate. The token cost of all enabled presets is added to every interaction.</Note>

## FAQ

<AccordionGroup>
  <Accordion title="Can I customize the content of a preset?">
    No — presets are fixed best-practice prompts. For custom instructions, write them directly in your agent's prompt. See the [Prompt Engineering Guide](/build/prompt-engineering-guide) for tips.
  </Accordion>

  <Accordion title="Do handbook presets conflict with my custom prompt?">
    Handbook presets work alongside your custom prompt. If your prompt gives instructions that overlap with a preset (e.g., you wrote your own empathy guidelines), you may want to disable the overlapping preset to avoid inconsistent behavior.
  </Accordion>

  <Accordion title="Why are some presets grayed out for my chat agent?">
    Five presets — Natural Filler Words, Echo Verification, NATO Phonetic Alphabet, Speech Normalization, and Smart Matching — are designed specifically for voice interactions and are not applicable to chat agents.
  </Accordion>
</AccordionGroup>


# Speech recognition provider comparison
Source: https://docs.retellai.com/build/asr-provider-comparison

Understand how Retell's speech recognition providers differ — Retell auto-routes to the best fit for your selected languages.

Retell automatically picks a speech recognition provider based on the languages your agent is configured for. You don't need to choose one manually, but it helps to understand the trade-offs when deciding which languages to support.

<Note>
  These observations are based on our internal testing and routing rules. Results may vary depending on the specific languages, audio conditions, and call patterns.
</Note>

## Provider overview

### Deepgram

* **Best for:** Lowest latency, the default for single-language agents on common languages.
* **Multilingual:** Supports code-switching across 10 languages: English, Spanish, French, German, Hindi, Russian, Portuguese, Japanese, Italian, Dutch.
* **Consideration:** Doesn't cover less-common languages (e.g., Welsh, Marathi, Kazakh).

### Azure

* **Best for:** The broadest single-language coverage — including languages no other provider supports (e.g., Icelandic, Nepali, Filipino).
* **Consideration:** No multilingual mode. Used only when the agent is configured with a single language.

### Soniox

* **Best for:** Multilingual code-switching across a much wider set than Deepgram — about 50 languages, with the same coverage in both single and multi modes.
* **Consideration:** Slightly higher latency than Deepgram, so Retell prefers Deepgram when both providers support a language.

## How Retell picks a provider

Retell evaluates the agent's selected languages against each provider's coverage and routes to the most accurate option:

* **Single common language** → Deepgram.
* **Single uncommon language** (not covered by Deepgram) → Azure.
* **Multiple languages, all within Deepgram's multilingual set** → Deepgram multilingual.
* **Multiple languages, broader combination** → Soniox.
* **Multiple variants of the same base language** (e.g., `en-US` + `en-GB`) → routed as single-language for that base, with no accuracy penalty.

If no single provider can cover all of your selected languages together, the dashboard prevents you from selecting that combination. See [Configure a multilingual agent](/agent/multilingual) for details.


# Book Calendar
Source: https://docs.retellai.com/build/book-calendar

Integrate Cal.com appointment booking with Retell AI.

This guide explains how to integrate cal.com's book appointment functionality into your application. This integration allows you to book appointments on cal.com.

<Frame>
  <img alt="Check availability tool interface" />
</Frame>

<Steps>
  <Step title="Create a Cal.com Account">
    1. Visit [cal.com](https://cal.com) to create an account
  </Step>

  <Step title="Configure Event Type">
    1. Navigate to the "Event Types" section in your cal.com dashboard
    2. Click "New"
    3. Configure your event settings
    4. Click "Save" to create the event type
  </Step>

  <Step title="Obtain Required Credentials">
    <Frame>
      <img alt="API credentials location" />
    </Frame>

    #### Get Event Type ID

    1. Open your created event type
    2. Look at the URL in your browser
    3. The event type ID is the number in the URL
       Example: `https://app.cal.com/your-username/event-type/1427703`
       In this case, `1427703` is your event type ID

    #### Get API Key

    1. Go to "Settings" in your cal.com dashboard
    2. Navigate to "Developer" section
    3. Click on "API Keys" to retrieve your API key
  </Step>

  <Step title="Add a book on calendar function in Retell">
    1. Enter the following details:
       * Tool name: this has to be unique within that agent
       * API Key from cal.com
       * Event Type ID
       * Tool description (example: "Book the appointment for 30-minute consultation calls")
       * (optional): add a timezone to be used in the function
    2. Click "Save" to complete the setup
  </Step>

  <Step title="Update prompt for function">
    It's best to include in the prompt explicitly when is the best time to invoke the custom function. For example:

    ```
    When user selected a slot, please book the appointment by calling the `book_appointment` function.
    ```
  </Step>
</Steps>

Video tutorial (based on single / multi prompt agent):

<iframe title="YouTube video player" />


# Check Calendar Availability
Source: https://docs.retellai.com/build/check-availability

Integrate Cal.com availability checking to find open time slots.

This guide explains how to integrate cal.com's calendar availability checking functionality into your application. This integration allows you to check available time slots for your cal.com event types.

<Frame>
  <img alt="Check availability tool interface" />
</Frame>

<Steps>
  <Step title="Create a Cal.com Account">
    1. Visit [cal.com](https://cal.com) to create an account
  </Step>

  <Step title="Configure Event Type">
    1. Navigate to the "Event Types" section in your cal.com dashboard
    2. Click "New"
    3. Configure your event settings
    4. Click "Save" to create the event type
  </Step>

  <Step title="Obtain Required Credentials">
    <Frame>
      <img alt="API credentials location" />
    </Frame>

    #### Get Event Type ID

    1. Open your created event type
    2. Look at the URL in your browser
    3. The event type ID is the number in the URL
       Example: `https://app.cal.com/your-username/event-type/1427703`
       In this case, `1427703` is your event type ID

    #### Get API Key

    1. Go to "Settings" in your cal.com dashboard
    2. Navigate to "Developer" section
    3. Click on "API Keys" to retrieve your API key
  </Step>

  <Step title="Add a check calendar availability function in Retell">
    1. Enter the following details:
       * Tool name: this has to be unique within that agent
       * API Key from cal.com
       * Event Type ID
       * Tool description (example: "Checks availability for 30-minute consultation calls")
       * (optional): add a timezone to be used in the function
    2. Click "Save" to complete the setup
  </Step>

  <Step title="Update prompt for function">
    It's best to include in the prompt explicitly when is the best time to invoke the custom function. For example:

    ```
    When user stated a time range, please check the calendar availability by calling the `check_calendar_availability` function and let user know whether that range work or not.
    ```
  </Step>
</Steps>

Video tutorial (based on single / multi prompt agent):

<iframe title="YouTube video player" />


# Call Transfer Node
Source: https://docs.retellai.com/build/conversation-flow/call-transfer-node



<Warning>
  This node only works during phone calls instead of web calls. It's available for Retell numbers and imported numbers.
</Warning>

Call transfer node is used to transfer the call to another number. The agent will not speak when it's in this node. If you want the agent to say things like `Let me transfer you right away` before performing the actual transfer, you can do so by putting a conversation node (with `skip response` turned on) before this node.

<Frame>
  <img />
</Frame>

## When Can Transition Happen

Transition happens when transfer fails. There's already a pre-populated edge for this, feel free to connect that to a node to handle transfer failure.

## Configure Transfer

<Steps>
  <Step title="Setup Transfer To Target">
    Set transfer number to be either:

    * a number in e.164 format, or a SIP URI in the format of `sip:username@domain` (e.g. `sip:user@retellai.com`).
    * [dynamic variable](/build/dynamic-variables) that gets substituted at runtime
    * (Optional) if your transfer destination is not in e.164 format then you can choose to keep the input as is by choosing raw format. This only applies when you are using custom telephony and does not apply when you are using Retell Telephony. This can be useful when you want to transfer to internal pseudo numbers. This can be useful when you want to transfer to internal pseudo numbers.

    <Frame>
      <img />
    </Frame>

    Set the transfer number extension if needed. Extension must be 0-9, '\*', '#' (E.g. 123#)
  </Step>

  <Step title="Configure Transfer Type">
    Choose between cold transfer, warm transfer, or agentic warm transfer:

    * **Cold transfer**: The call is transferred to a destination number and that's it.
    * **Warm transfer**: After the call is transferred to the destination number, the AI agent can attempt to detect if the other side is human, leave private messages that are not heard by user, do a three-way introduce, etc. This is a direct warm transfer flow (not agentic warm transfer). (more details below).
    * **Agentic warm transfer**: A transfer agent has a two-way conversation with the transfer target and then decides to either bridge the original caller or cancel the transfer.
  </Step>

  <Step title="Configure Transfer Dial Timeout (All Modes)">
    Use this slider to set how long the destination should ring for this transfer.

    * The value you set here applies only to this transfer.
    * If you do not set it, we use your agent-level ring duration setting.
    * This works for cold transfer, warm transfer, and agentic warm transfer.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Caller ID (Optional)">
    You can configure which caller id shows up to the transfer destination:

    1. **Retell Agent's number**: The transfer destination will see the Retell agent's number

    2. **User's Number**: The transfer destination will see the number of the user. Please note that the telephony provider must support caller id override for this feature to work.
       * For warm transfer, it's using SIP DIAL, and we are setting `from` and `P-Asserted-Identity` headers to the user's number.
       * For cold transfer, it's using SIP REFER, and it's up to the telephony provider to support caller id override for SIP REFER.
       * Retell Twilio numbers support showing user's number on both warm and cold transfer, Retell Telnyx numbers only support this when using SIP REFER via cold transfer.
       * If caller id override is not supported, the transfer would fail.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Cold Transfer Specific Settings">
    For cold transfer, you can configure the following settings:

    * **Cold transfer modes**: You can choose `SIP INVITE` or `SIP REFER`.
    * **What SIP is**: SIP (Session Initiation Protocol) is the signaling protocol used to set up and route VoIP calls.
    * **SIP INVITE**: This is the default transfer method. It establishes or updates the active call path, then bridges the transfer. You can choose which caller ID to use.
    * **SIP REFER**: This asks an endpoint to start a separate call to a third party for transfer handoff. Use this only if your telephony provider supports SIP REFER. Caller ID behavior depends on provider support and configuration.
    * **Caller ID behavior**: `show transferee as caller` only applies when cold transfer mode is `SIP INVITE`.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Warm Transfer Specific Settings (Non-Agentic)">
    For warm transfer (non-agentic), you can configure the following settings:

    * **On-hold music**: The audio played to the caller while they are on hold. The default is a standard ringtone.
    * **Navigate IVR**: Provide an prompt to help you navigate if the transfer target is an IVR system.
    * **Enable human detection**: When enabled, the agent will check if a human is present after the transfer target answers. The original caller will only be connected once a human is detected.
    * **Auto-greet**: If enabled, the agent will immediately say “Hello” when the transfer target picks up. This encourages a response, increasing the likelihood of detecting a human.
    * **Agent detection timeout**: The maximum amount of time the AI agent will wait to determine whether the transfer target is a human. The caller is connected only if human detection succeeds within this timeframe. Otherwise, the transfer is marked as failed. The default timeout is 30 seconds.
    * **Whisper message (optional)**: A message spoken privately to the transfer target before connecting them to the original caller.
    * **Three-way message (optional)**: A message spoken to both the transfer target and the original caller once the connection is established.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Agentic Warm Transfer Specific Settings">
    For agentic warm transfer, you can configure the following settings:

    * **On-hold music**: The audio played to the original caller while the transfer agent is working.
    * **Two-way conversation agent**: Select the transfer agent (and version) that has a two-way conversation with the transfer target and decides whether to bridge or cancel.
    * **Wait time for agent answer**: Set how long to wait for the transfer agent to make a decision.
    * **Three-way ring tone**: While the transfer agent is handling the handoff, the original caller hears the selected ring tone/on-hold audio until the call is bridged or canceled.
    * **Three-way message (optional)**: A message shared with both parties when the call is bridged.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Add Custom SIP Headers (Optional)">
    Add custom SIP headers for outbound calls. Custom SIP headers (usually prefixed with `X-`) let you pass session-specific data, such as user IDs or campaign codes, between VoIP endpoints.
    These headers are forwarded to your SIP provider on SIP INVITE and are useful for custom routing and tagging.

    <Warning>Custom SIP headers are preserved only when transferring the call directly to a SIP endpoint. They may be stripped if you are transferring the call to a PSTN number.</Warning>

    <code>All header names must start with `X-` or must be `User-To-User` (case insensitive)</code>

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>

## Rest of Node Settings

* **Speak During Execution**: when enabled, a text input box will show up where you can write instructions for the agent to follow to generate an utterance like `Let me check that for you.` to say while the function is being executed. You can choose between `Prompt` and `Static Sentence`.
* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **LLM**: choose a different model for this particular node. Will be used for function argument generation, and potentially speak during execution message generation.


# Code Node
Source: https://docs.retellai.com/build/conversation-flow/code-node

Execute JavaScript code directly in your conversation flow without an external server

Code node executes JavaScript code when the agent enters it. Unlike [custom functions](/build/conversation-flow/custom-function), code nodes run directly in Retell's sandbox — no external server needed. The node is not intended for having a conversation with the user, but the agent can still talk while code is running if needed.

<Frame>
  <img alt="Code node on the conversation flow canvas" />
</Frame>

## Code Node vs Custom Function

|                   | Code Node                                                   | Custom Function                                  |
| ----------------- | ----------------------------------------------------------- | ------------------------------------------------ |
| **Runs**          | JavaScript in Retell's sandbox                              | HTTP request to your server                      |
| **Requires**      | Nothing — runs directly                                     | Your own API endpoint                            |
| **Best for**      | Data transformation, simple API calls, logic & calculations | Complex integrations, accessing internal systems |
| **Max code size** | 5,000 characters                                            | N/A (runs on your server)                        |

<Warning>
  Code Node is designed for lightweight logic like formatting, calculations, and simple read-only lookups. Do not use it to access internal systems, write to production databases, or handle sensitive credentials. Both `dv` and `metadata` values are stored in plaintext with every call record. For integrations that require authentication, secrets management, or write access, use a [Custom Function](/build/conversation-flow/custom-function) hosted on your own backend. See [Security and Architecture Guidance](#security-and-architecture-guidance) for details.
</Warning>

## Write Your Code

<Steps>
  <Step title="Add a Code Node">
    Click the Code node from the left sidebar to add it to the canvas.

    <Frame>
      <img alt="Left sidebar showing the Code node option" />
    </Frame>
  </Step>

  <Step title="Open the code editor">
    Click **Open** on the code node to launch the code editor.
  </Step>

  <Step title="Write JavaScript">
    Write your JavaScript code in the editor. You have access to dynamic variables, call metadata, and the `fetch` function for HTTP requests. See [JavaScript Environment](#javascript-environment) below for details.

    <Frame>
      <img alt="Code editor with JavaScript code and configuration options" />
    </Frame>

    ```javascript theme={null}
    // Example: look up an order and return the status
    const response = await fetch("https://api.example.com/orders/" + dv.order_id);
    const data = await response.json();
    return { status: data.status, estimated_delivery: data.delivery_date };
    ```
  </Step>

  <Step title="Set response variables (optional)">
    Use **Store Fields as Variables** to extract values from your code's return value and save them as dynamic variables. Specify a variable name and the JSON path to the value.

    For example, if your code returns `{ "status": "shipped", "estimated_delivery": "March 25" }`:

    | Variable Name   | JSON Path            | Extracted Value |
    | --------------- | -------------------- | --------------- |
    | `order_status`  | `status`             | `"shipped"`     |
    | `delivery_date` | `estimated_delivery` | `"March 25"`    |

    These variables can then be referenced as `{{order_status}}` and `{{delivery_date}}` in other nodes.
  </Step>

  <Step title="Test your code">
    Click **Run Code** at the bottom of the editor to test. Use the **Dynamic Variables** dropdown in the editor to set test values for your variables (e.g., give `customer_name` a value of "John Doe") — these values are only used during testing and won't affect your live agent. The output panel will show the result and any `console.log()` output.

    <Frame>
      <img alt="Code editor showing test output after clicking Run Code" />
    </Frame>
  </Step>
</Steps>

## JavaScript Environment

Your code runs in a JavaScript sandbox with the following globals available. The code editor provides **autocomplete** — as you type, it will suggest available globals, dynamic variable names, and built-in functions.

### `dv` — Dynamic Variables

Access your agent's dynamic variables as properties on the `dv` object. All values are strings.

```javascript theme={null}
const name = dv.customer_name;       // "John Doe"
const orderId = dv.order_id;         // "78542"
const total = parseFloat(dv.amount); // Convert to number if needed
```

### `metadata` — Call Metadata

Access metadata passed when the call was created via the API. This is the same object you pass in the `metadata` field of the [Create Call](/api-references/create-phone-call) API.

```javascript theme={null}
const customerId = metadata.customer_id;
const priority = metadata.priority_level;
```

<Warning>
  Both `dv` and `metadata` values are stored in plaintext with every call record and are visible in call logs and API responses. Do not use them to pass API keys, database credentials, or other sensitive secrets. See [Security and Architecture Guidance](#security-and-architecture-guidance) for more details.
</Warning>

### `fetch(url)` — HTTP Requests

Make HTTP requests to external APIs. Works like the standard [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API).

```javascript theme={null}
// GET request
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// POST request
const response = await fetch("https://api.example.com/submit", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: dv.customer_name })
});
```

### `console.log()` — Debugging

Log output for debugging. Logs appear in the test output panel when using **Run Code**, and are also available in call logs.

```javascript theme={null}
console.log("Customer:", dv.customer_name);
console.log("API response:", JSON.stringify(data));
```

<Note>
  * Your code can return any value (object, string, number) or return nothing at all.
  * Standard JavaScript built-ins are available: `Math`, `JSON`, `Date`, `Array`, `Object`, `String` methods, etc.
  * External packages (`require`, `import`) are **not** available. Use `fetch()` for external integrations.
  * Code is limited to 5,000 characters.
</Note>

## Examples

### Format data from dynamic variables

```javascript theme={null}
// Combine and format customer info
const fullName = dv.first_name + " " + dv.last_name;
const summary = `Customer ${fullName} (ID: ${dv.customer_id}) requested a callback.`;
return { full_name: fullName, summary: summary };
```

### Fetch data from a public API

```javascript theme={null}
// Look up current weather for the customer's city
const response = await fetch("https://api.weatherapi.com/v1/current.json?q=" + encodeURIComponent(dv.city));
const weather = await response.json();
return {
  location: weather.location.name,
  temperature: weather.current.temp_f + "°F",
  condition: weather.current.condition.text
};
```

### Conditional logic with API call

```javascript theme={null}
// Route based on customer tier
const response = await fetch("https://api.example.com/customers/" + dv.customer_id);
const customer = await response.json();

if (customer.tier === "premium") {
  return { action: "priority_support", wait_time: "0 minutes" };
} else if (customer.tier === "standard") {
  return { action: "standard_queue", wait_time: "5 minutes" };
} else {
  return { action: "general_queue", wait_time: "10 minutes" };
}
```

## Security and Architecture Guidance

Code Node is best for lightweight, low-risk logic that runs entirely within Retell's sandbox. As your integration needs grow, use a [Custom Function](/build/conversation-flow/custom-function) hosted on your own backend where you control the security boundary.

| Use case                                                                             | Recommended             |
| ------------------------------------------------------------------------------------ | ----------------------- |
| Formatting, calculations, string cleanup                                             | Code Node               |
| Simple read-only lookups to low-risk public APIs                                     | Code Node, with caution |
| Accessing internal systems or private APIs                                           | Custom Function         |
| Writing to CRM, EHR, booking, payment, or ticketing systems                          | Custom Function         |
| Workflows requiring secrets, audit logs, retries, idempotency, or policy enforcement | Custom Function         |

<Warning>
  **Do not treat dynamic variables or metadata as a secret vault.** Avoid placing long-lived API keys, database credentials, or other sensitive secrets in dynamic variables or call metadata for use in Code Node. Both `dv` and `metadata` values are stored in plaintext with every call record — anything you pass in will be visible in call logs and API responses. They are not designed for secret management. Prefer short-lived tokens where possible, and use a [Custom Function](/build/conversation-flow/custom-function) for integrations that require sensitive credentials or customer-controlled secret handling.
</Warning>

<Warning>
  **Use `fetch()` with caution.** Enabling outbound HTTP requests from an LLM-invoked tool increases security and operational risk. Treat any use of `fetch()` as an external integration surface. Prefer read-only requests to low-risk, public endpoints. Avoid direct state-changing actions (writes, payments, deletions) unless you fully understand the risks and have appropriate controls in place.
</Warning>

<Note>
  **Keep production logic in your own backend.** For anything involving sensitive credentials, direct writes to production systems, payment actions, regulated data workflows, or business-critical operations that require strict authentication, validation, audit logging, idempotency, or approval controls — use a [Custom Function](/build/conversation-flow/custom-function) hosted on your own backend. Code Node should be reserved for data transformation, calculations, and simple read-only lookups.
</Note>

## Response Variables

Response variables let you extract specific values from your code's return value and store them as dynamic variables for use in other nodes.

Specify each variable as a **name** and a **JSON path** using dot notation:

| Path Syntax     | Example         | Extracts               |
| --------------- | --------------- | ---------------------- |
| Top-level field | `status`        | `result.status`        |
| Nested field    | `data.order.id` | `result.data.order.id` |
| Array element   | `items[0].name` | First item's name      |

If a path doesn't exist in the return value, the variable is skipped (no error).

## When Can Transition Happen

* If **Wait for Result** is turned off:
  * If **Speak During Execution** is on, the agent transitions once done talking
  * If **Speak During Execution** is off, the agent transitions immediately after code starts running
  * If the user interrupts the agent, transition can happen once the user is done speaking
* If **Wait for Result** is turned on:
  * If **Speak During Execution** is on, the agent transitions once code finishes and agent is done talking
  * If **Speak During Execution** is off, the agent transitions once code finishes
  * If the user interrupts the agent, transition can happen once code finishes and user is done speaking

Since the code node considers the code result for transition timing, you can write [transition conditions](/build/conversation-flow/transition-condition) based on the code result or the extracted dynamic variables.

## Node Settings

* **Speak During Execution**: When enabled, the agent says something while the code runs (e.g., "Let me check that for you."). Choose between **Prompt** (LLM generates the message) or **Static Text** (exact text you provide).
* **Wait for Result**: When enabled, the agent waits for the code to finish before transitioning. This guarantees that when you reach the next node, the result and extracted variables are ready.
* **Timeout**: How long the code can run before timing out. Range: 5–60 seconds. Default: 30 seconds.
* **Global Node**: Read more at [Global Node](/build/conversation-flow/global-node).
* **Block Interruptions**: When enabled, the agent will not be interrupted by the user when speaking.
* **LLM**: Choose a different model for this node. Used for speak during execution message generation if set to Prompt.
* **Fine-tuning Examples**: Can finetune transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples).

## FAQ

<AccordionGroup>
  <Accordion title="Can I use npm packages or external libraries?">
    No. The code runs in a lightweight JavaScript sandbox without access to `require` or `import`. You can use all standard JavaScript built-ins (`Math`, `JSON`, `Date`, `Array` methods, etc.) and the `fetch()` function for external API calls.
  </Accordion>

  <Accordion title="What happens if my code times out?">
    If your code exceeds the configured timeout (default 30 seconds), it will be stopped and treated as a failed execution. The result will contain a timeout error message. You can adjust the timeout in Node Settings (5–60 seconds).
  </Accordion>

  <Accordion title="What happens if my code throws an error?">
    If your code throws an error or crashes, the execution is marked as failed and the error message is returned as the result. Response variables will not be extracted. You can use `try/catch` in your code to handle errors gracefully.
  </Accordion>

  <Accordion title="Can I use async/await?">
    Yes. The `fetch()` function is async, so you can use `await` to wait for HTTP responses. Top-level `await` is supported.
  </Accordion>

  <Accordion title="Is there a limit on the result size?">
    Yes, the result is capped at 15,000 characters to prevent overloading the LLM context.
  </Accordion>
</AccordionGroup>


# Components
Source: https://docs.retellai.com/build/conversation-flow/components

Build reusable sub-flows to keep agents maintainable and consistent

## Conversation Flow Components

Make complex agents easier to build, reuse, and maintain by packaging parts of your conversation into Components. A Component is a mini flow (a group of nodes) that you can reuse across agents and flows.

### Why use Components?

* Reuse: Build once, drop into many agents and flows.
* Consistency: Keep behavior uniform across use cases (e.g., identity check).
* Clean canvas: Hide detailed logic inside a focused sub-flow.
* Faster iteration: Update a shared Component to improve every agent that uses it.

### Where to find it

<Frame>
  <img />
</Frame>

In the dashboard, open your agent’s builder:

* Left sidebar → Components tab
* Two sections:
  * Library Components: Account-level, shared across agents.
  * Agent Components: Local to the current agent.

## Create a Component

You can create either a library (shared) Component or an agent-level (local) one. Both open in a dedicated editor tab.

* Create a Component:
  1. In Components, click + Create.
  2. You’ll start with a "Begin" node, a basic conversation node and an “Exit Component” end node.
  3. Add nodes and connect edges to form your sub-flow.
  4. Set a start node by connecting the Begin tag to the first node.
  5. Make sure you link "Exit" node correctly so that you won't stuck at this component.
  6. You can switch back to the main agent by click the bottom navigation bar.
  7. You can rename the component by clicking the "..." on the right of the Component name.

Notes:

* Components cannot contain other Components; you add regular nodes inside a Component.
* Available node types match your agent’s channel (voice vs chat).

<Frame>
  <img />
</Frame>

## Add a Component to your flow

* From the Components tab, click a Component. A single Component node appears in your canvas.
* Connect into the Component: link any node to the Component node.
* Connect out of the Component: select the Component node and connect its outgoing edge to where the conversation should continue.
* To edit what happens inside, click "Edit Component" (or open the Component tab) and modify its internal nodes.
* You can modify the Component node name, which will also be reflected in the Component.

Tip: End nodes inside the Component hand control back to the main flow. Back on the main canvas, make sure the Component node’s outgoing edge points to the next step.

<Frame>
  <img />
</Frame>

## Shared vs Local Components

**Shared (Library Components)**:

* Account-level. Reusable across multiple agents.
* Edits sync to every agent that uses it — great for universal steps.

**Local (Agent Components)**:

* Live only in the current agent.
* Edits affect this agent only.

**Convert Between Shared & Local**:

* Turn on “Save component to library” to create a shared (library) version.
* Turn off syncing to convert the reference in your agent to a local copy that stops receiving updates.

<Frame>
  <img />
</Frame>

**Deletion Behavior**:

* Deleting a shared Component from the library downgrades linked instances in agents to local copies and stops sync updates (your agents keep working).

**Publish Agent**:

When you publish an agent, we protect production behavior and keep draft work flexible:

* Published version snapshots shared Components as local copies.
  * This prevents future library updates from changing already-published calls.
  * The published artifact is stable and won’t auto-update from the library.
* Your latest editable draft stays linked to the shared Component.
  * You continue to benefit from library updates while iterating.
  * When you’re ready, publish again to roll out the latest changes.

Recommended workflow:

* Build using Library Components → test → Publish → keep iterating in draft.
* Publish again whenever you want to promote the latest shared/local changes to production.

## Testing

* In order to test the component under the component panel, the component need to be added to the main Conversation Flow so that it would be initialized properly.
* The global prompt of the main Conversation Flow will be applied to all the component nodes implicitly.
* If you want to test the component alone, you can make it a shared component and create a new empty agent with only one component node.

## Best practices

* Keep Components focused: One clear job (e.g., “Collect Shipping Address”).
* Name clearly: Use action + outcome (e.g., “Verify Identity”).
* Design clean entry/exit: Always set a start node; include an end node to exit cleanly.
* Reuse variables: Use dynamic variables to pass captured data back to the main flow.
* Test in context: Open Test panel to simulate end-to-end behavior after inserting the Component.

## FAQ

* How do I update a shared Component used by many agents?
  * Under any agent, you can navigate to the component edit page. When you editing, changes apply everywhere it’s used.

* Can I stop changes from affecting an agent?
  * Yes. In that agent, turn off syncing to convert its reference to a local copy.

* What happens if I delete a library Component?
  * Agents keep a local copy; they stop syncing with the deleted library item.

* Can I move a local Component into the library?
  * Yes. Use “Save component to library” to create a shared version and update references.

* Can Components include tools/functions?
  * Yes. Components can include function nodes and use your configured tools. Tools behave the same as in the main flow.
  * The tools need to be defined within the component and will not be visible outside at agent level.

* What if I did not link the Begin node in a component?
  * It transitions to the next node based on the Component node edges.

* What if I did not link the Exit node properly in a component?
  * It will stay stuck inside the component and cannot transition out.


# Conversation Node
Source: https://docs.retellai.com/build/conversation-flow/conversation-node



Conversation node is the most commonly used node type in conversation flow. It's used to have a conversation with the user without tool calling during the conversation.

If you want the agent to talk to the user and call tools during the same node, use a [Subagent Node](/build/conversation-flow/subagent-node).

Please note that agent can have a multi turn conversation inside a single node, so you don't necessarily need to create a new conversation node for every sentence the agent needs to say. It's recommended to split node when there's logic split, or the instruction got too long.

<img />

## Write Instruction

Inside the node, you get to pick how you want to write the specific instruction for the agent to follow:

* **Prompt**: Write a prompt for the agent to dynamically generate what to say.
* **Static Sentence**: Agent will say a fixed sentence first, and if later still inside this node, it will generate content dynamically based on the static sentence set.

## When Can Transition Happen

* when user is done speaking
* when `Skip Response` is enabled and agent finishes speaking

## Node Settings

* **Skip Response**: when enabled, the transition will only have one edge that you can connect, and when agent is done talking, it will transition to the next node via that specific edge. This is useful when you want the agent to say things like disclaimers, where you don't need a response to move on to another node.
* **Knowledge Base**: configure node-level knowledge bases to combine topic-specific knowledge with the agent-level knowledge base. Read more at [Knowledge Base](/build/knowledge-base).
* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **Block Interruptions**: when enabled, the agent will not be interrupted by user when speaking.
* **LLM**: choose a different model for this particular node. Will be used for response generation.
* **Fine-tuning Examples**: Can finetune conversation response, and transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)


# Custom Function
Source: https://docs.retellai.com/build/conversation-flow/custom-function



Custom functions allow you to extend your agent's capabilities by integrating external APIs, providing additional knowledge, or implementing custom logic.

## Steps to create a custom function

When a custom function is called, Retell sends a request (POST, GET, PUT, PATCH, DELETE) to your specified URL with the function name and parameters.
You can include headers and query parameters in the request, and extract data from the response.

<Steps>
  <Step title="Configure function details">
    Add a name and description for the custom function. The name should be unique and separated with underscore.

    <Frame>
      <img alt="Custom function configuration showing name and description fields" />
    </Frame>

    For example:

    * Name: `get_user_details`
    * Description: `Get user details based on name and age`
  </Step>

  <Step title="Select HTTP Method">
    Choose the HTTP method that Retell will use to send the request to your endpoint. Available methods include:

    <ul>
      <li><strong>GET</strong></li>
      <li><strong>POST</strong></li>
      <li><strong>PATCH</strong></li>
      <li><strong>PUT</strong></li>
      <li><strong>DELETE</strong></li>
    </ul>
  </Step>

  <Step title="Add endpoint URL">
    Add the URL where Retell will send the request to execute your custom function. This has to be a valid URL.
  </Step>

  <Step title="Set request headers (optional)">
    You can define custom headers to include with the request Retell sends to your endpoint.
    Header values can be static or include dynamic variables.

    <Frame>
      <img alt="Custom request headers configuration with static and dynamic variable values" />
    </Frame>
  </Step>

  <Step title="Set query parameters (optional)">
    You can define query parameters to include in the request URL that Retell appends to your endpoint.
    There is a switch to change between parameter description or const value. Both description and const value could be dynamic variables.
    Description will be resolved by LLM while const value will be applied directly to the function.

    <Frame>
      <img alt="Query parameter configuration with toggle between description and const value" />
    </Frame>
  </Step>

  <Step title="Define parameters">
    Define the parameters for the custom function using JSON schema format or JSON form. Only available for POST, PATCH and PUT requests. For guidance, refer to:

    * [OpenAI's Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
    * [Function Calling Tutorial](https://semaphoreci.com/blog/function-calling)

    **Payload: args only**

    When **Payload: args only** is enabled, the JSON body is only the function's arguments: those fields appear at the top level of the request, not nested under `args`. When it is off, the body follows **Request & response spec** below (`name`, `call`, and `args`).

    <Tip>
      Turn this on when your endpoint expects a flat JSON body that matches your parameter object exactly, with no outer wrapper.
    </Tip>

    Example parameter schema:

    ```json theme={null}
    {
      "type": "object",
      "required": [
        "order_id"
      ],
      "properties": {
        "name": {
          "type": "object",
          "description": "",
          "properties": {
            "first_name": {
              "type": "string",
              "description": "User first name"
            },
            "last_name": {
              "type": "string",
              "const": "{{last_name}}"
            }
          }
        },
        "order_id": {
          "type": "number",
          "const": 1234
        }
      }
    }
    ```

    Example JSON form:

    <Frame>
      <img alt="JSON form interface for defining function parameters" />
    </Frame>
  </Step>

  <Step title="Set response variables (optional)">
    Extract values from the API response and save them as <strong>dynamic variables</strong> for use later in the conversation.

    For example, you can extract a user’s name from the response and reference it later using <code>\{\{user\_name}}</code>.

    Example response body

    ```javascript theme={null}
    {
      "properties": {
        "user": {
          "name": "John Doe",
          "age": 26
        }
      }
    }
    ```

    <Frame>
      <img alt="Response variable extraction mapping API response fields to dynamic variables" />
    </Frame>
  </Step>
</Steps>

### Troubleshooting

If you failed to save the custom function, it is likely because the parameters are not valid.

One common mistake is not adding `"type": "object",` to the top level of the JSON schema. We recommend clicking one of the examples and update accordingly.

## Request & response spec

Retell will send the request to your endpoint with the following request spec.

**Request**

* header
  * `X-Retell-Signature`: encrypted request body using your secret key, used to verify the request is from Retell. Read more below.
  * Content-Type: application/json. This indicates the payload is in JSON format.
* body (in JSON format, for POST, PUT and PATCH request)
  * `name`: the name of the custom function.
  * `call`: the call object for you to get more context about the call, it also contains real time transcript up to the time the request is sent. Check out [Get Call API](/api-references/get-call) for more details about the call object.
  * `args`: the arguments for the custom function, as a JSON object.

<Note>
  If **Payload: args only** is enabled for a function, the body is only the argument object (no `name`, `call`, or `args` wrapper). Parse parameters from the top level of the JSON, and run signature verification on that same body string.
</Note>

<Accordion title="Example request body">
  ```json theme={null}
  {
    "name": "analyze_transcript",
    "args": {
      "analysis_type": "sentiment"
    },
    "call": {
      "call_type": "web_call",
      "access_token": "eyJhbGciOiJIUzI1NiJ9.eyJ2aWRlbyI6eyJyb29tSm9p",
      "call_id": "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6",
      "agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
      "agent_version": 1,
      "agent_name": "My Agent",
      "call_status": "ongoing",
      "metadata": {
        "internal_customer_id": "cust_12345"
      },
      "retell_llm_dynamic_variables": {
        "customer_name": "John Doe"
      },
      "custom_sip_headers": {
        "X-Custom-Header": "Custom Value"
      },
      "data_storage_setting": "everything",
      "opt_in_signed_url": true,
      "start_timestamp": 1703302407333,
      "transcript": "Agent: Hi John, thanks for calling! How can I help you today?\nUser: Hi, I'd like to check the status of my recent order.\nAgent: Sure, I'd be happy to help with that. Could you provide me your order number?\nUser: Yes, it's 78542.\nAgent: Let me look that up for you.\n",
      "transcript_object": [
        {
          "role": "agent",
          "content": "Hi John, thanks for calling! How can I help you today?",
          "words": [
            { "word": "Hi", "start": 0.5, "end": 0.7 },
            { "word": "John,", "start": 0.8, "end": 1.1 },
            { "word": "thanks", "start": 1.2, "end": 1.5 },
            { "word": "for", "start": 1.5, "end": 1.6 },
            { "word": "calling!", "start": 1.7, "end": 2.1 },
            { "word": "How", "start": 2.2, "end": 2.4 },
            { "word": "can", "start": 2.4, "end": 2.5 },
            { "word": "I", "start": 2.5, "end": 2.6 },
            { "word": "help", "start": 2.6, "end": 2.8 },
            { "word": "you", "start": 2.8, "end": 2.9 },
            { "word": "today?", "start": 2.9, "end": 3.3 }
          ]
        },
        {
          "role": "user",
          "content": "Hi, I'd like to check the status of my recent order.",
          "words": [
            { "word": "Hi,", "start": 4.0, "end": 4.3 },
            { "word": "I'd", "start": 4.4, "end": 4.6 },
            { "word": "like", "start": 4.6, "end": 4.8 },
            { "word": "to", "start": 4.8, "end": 4.9 },
            { "word": "check", "start": 4.9, "end": 5.2 },
            { "word": "the", "start": 5.2, "end": 5.3 },
            { "word": "status", "start": 5.3, "end": 5.7 },
            { "word": "of", "start": 5.7, "end": 5.8 },
            { "word": "my", "start": 5.8, "end": 5.9 },
            { "word": "recent", "start": 5.9, "end": 6.2 },
            { "word": "order.", "start": 6.2, "end": 6.6 }
          ]
        },
        {
          "role": "agent",
          "content": "Sure, I'd be happy to help with that. Could you provide me your order number?",
          "words": [
            { "word": "Sure,", "start": 7.0, "end": 7.4 },
            { "word": "I'd", "start": 7.5, "end": 7.7 },
            { "word": "be", "start": 7.7, "end": 7.8 },
            { "word": "happy", "start": 7.8, "end": 8.1 },
            { "word": "to", "start": 8.1, "end": 8.2 },
            { "word": "help", "start": 8.2, "end": 8.4 },
            { "word": "with", "start": 8.4, "end": 8.6 },
            { "word": "that.", "start": 8.6, "end": 8.9 },
            { "word": "Could", "start": 9.0, "end": 9.2 },
            { "word": "you", "start": 9.2, "end": 9.3 },
            { "word": "provide", "start": 9.3, "end": 9.6 },
            { "word": "me", "start": 9.6, "end": 9.7 },
            { "word": "your", "start": 9.7, "end": 9.9 },
            { "word": "order", "start": 9.9, "end": 10.2 },
            { "word": "number?", "start": 10.2, "end": 10.6 }
          ]
        },
        {
          "role": "user",
          "content": "Yes, it's 78542.",
          "words": [
            { "word": "Yes,", "start": 11.5, "end": 11.8 },
            { "word": "it's", "start": 11.9, "end": 12.1 },
            { "word": "78542.", "start": 12.2, "end": 12.9 }
          ]
        },
        {
          "role": "agent",
          "content": "Let me look that up for you.",
          "words": [
            { "word": "Let", "start": 13.5, "end": 13.7 },
            { "word": "me", "start": 13.7, "end": 13.8 },
            { "word": "look", "start": 13.8, "end": 14.0 },
            { "word": "that", "start": 14.0, "end": 14.2 },
            { "word": "up", "start": 14.2, "end": 14.3 },
            { "word": "for", "start": 14.3, "end": 14.5 },
            { "word": "you.", "start": 14.5, "end": 14.8 }
          ]
        }
      ],
      "transcript_with_tool_calls": [
        {
          "role": "agent",
          "content": "Hi John, thanks for calling! How can I help you today?",
          "words": [
            { "word": "Hi", "start": 0.5, "end": 0.7 },
            { "word": "John,", "start": 0.8, "end": 1.1 }
          ]
        },
        {
          "role": "user",
          "content": "Hi, I'd like to check the status of my recent order.",
          "words": [
            { "word": "Hi,", "start": 4.0, "end": 4.3 }
          ]
        },
        {
          "role": "agent",
          "content": "Sure, I'd be happy to help with that. Could you provide me your order number?",
          "words": [
            { "word": "Sure,", "start": 7.0, "end": 7.4 }
          ]
        },
        {
          "role": "user",
          "content": "Yes, it's 78542.",
          "words": [
            { "word": "Yes,", "start": 11.5, "end": 11.8 }
          ]
        },
        {
          "role": "agent",
          "content": "Let me look that up for you.",
          "words": [
            { "word": "Let", "start": 13.5, "end": 13.7 }
          ]
        },
        {
          "role": "tool_call_invocation",
          "tool_call_id": "tool_call_abc123",
          "name": "analyze_transcript",
          "arguments": "{\"analysis_type\": \"sentiment\"}"
        }
      ],
      "latency": {
        "e2e": {
          "p50": 650,
          "p90": 900,
          "p95": 1100,
          "p99": 1500,
          "max": 1600,
          "min": 400,
          "num": 3,
          "values": [400, 650, 1600]
        }
      }
    }
  }
  ```
</Accordion>

The request will timeout in your specified timeout period, or 2 minutes if not specified. When request fails, it will be retried up to 2 times.

**Response**

Response should have a status code between 200-299 to indicate success of HTTP request.
Response to the request can be in various format:

* string
* buffer
* JSON object
* blob

All these formats will be converted to string before sending to LLM for further processing.

<Note>
  The function result is capped at 15000 characters to prevent overloading LLM context window.
</Note>

## Verifying Request is from Retell

To verify that the request is coming from Retell, you can check the `X-Retell-Signature` header. The value is a encrypted request body using your secret key.

The value is a encrypted request body using your secret key.
For `GET` and `DELETE` requests, the request body is empty. You can use empty string in the verify function.

```javascript theme={null}
import { Retell } from "retell-sdk";
import express from "express";

const app = express();
// Use raw body for signature verification, not JSON.stringify(req.body).
app.use(express.raw({ type: "application/json" }));

app.post("/check-weather", async (req, res) => {
  const rawBody = req.body.toString("utf-8");
  if (
    !Retell.verify(
      rawBody,
      process.env.RETELL_API_KEY,
      req.headers["x-retell-signature"],
    )
  ) {
    console.error("Invalid signature");
    return;
  }
  const content = JSON.parse(rawBody);
  if (content.args.city === "New York") {
    return res.json("25f and sunny");
  } else {
    return res.json("20f and cloudy");
  }
});
```

```Python theme={null}
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from retell import Retell

retell = Retell(api_key=os.environ["RETELL_API_KEY"])

@app.post("/check-weather")
async def check-weather(request: Request):
    try:
        raw_body = (await request.body()).decode("utf-8")
        valid_signature = retell.verify(
            raw_body,
            api_key=str(os.environ["RETELL_API_KEY"]),
            signature=str(request.headers.get("X-Retell-Signature")),
        )
        if not valid_signature:
            print("Received Unauthorized")
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        post_data = json.loads(raw_body)
        args = post_data["args"]
        if args["city"] == "New York":
            return JSONResponse(status_code=200, content={"result": "25f and sunny"})
        else:
            return JSONResponse(status_code=200, content={"result": "20f and cloudy"})
    except Exception as err:
        print(f"Error in webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
```

<Note>You can also secure your server from public network by only allowlisting Retell IP addresses: `100.20.5.228`</Note>


# Debug guide
Source: https://docs.retellai.com/build/conversation-flow/debug-guide

How to improve your conversation flow agent's performance

Conversation flow is a powerful and flexible tool, which means that there's a lot of action items one can take when the agent's performance is not meeting your expectation. This guide is designed to help you identify the root cause of the issue, and provide actionable steps to improve the agent's responses and transitions.

<Note>This guide only covers the response part of the agent, if you have issues with agent audio, like pronunciation, please refer to other guides.</Note>

## Step 1: Identify the issue

When the agent is not responding as expected, there can be several reasons:

* The agent is not following instructions within a node
* Node transitions are not working as expected
* The actual conversation does not match the flow graph (e.g., users deviate from expected steps)

## Step 2: Fix the issue

Note that these issues are not mutually exclusive - you may need to implement multiple solutions to fully resolve the problem.

### Issue: Agent is not following instructions within a node

#### Split the node into multiple nodes

For example, if a node contains instructions to collect customer name, phone number, and address, the agent might inconsistently ask for only some of this information:

<Frame>
  <img alt="One node" />
</Frame>

You can improve consistency by splitting this into three separate nodes:

<Frame>
  <img alt="Three nodes" />
</Frame>

#### Change the node model

If the instructions are concise but the agent struggles to follow them, try using a more capable LLM model for this node.

#### Add conversation finetune examples

To achieve a specific response style, add conversation finetune examples. Learn more in our [Finetune Examples](/build/conversation-flow/finetune-examples) guide.

#### Adjust the LLM temperature

If the agent's responses are inconsistent, try adjusting the LLM temperature:

<img />

### Issue: Node transitions are not working as expected

If the agent isn't transitioning to the expected node, try these solutions:

* Review your transition conditions: Ensure they precisely match your intended triggers. Consider prompt engineering or breaking down complex conditions into multiple simpler ones.
* Add transition finetune examples: Provide examples to help the model understand your expectations. See our [Finetune Examples](/build/conversation-flow/finetune-examples) guide.

To handle missing transition scenarios:

* Add more nodes to cover edge cases, particularly global nodes for handling unexpected situations. Learn more about [Global Nodes](/build/conversation-flow/global-node).
* Make transition conditions more flexible and general.

### Issue: Actual conversation does not match the flow graph

When users deviate from the defined flow:

* Add key steps as global nodes to allow users to skip or jump between nodes. This is particularly useful for inbound support cases without a rigid call structure. See our [Global Node](/build/conversation-flow/global-node) guide.
* Make node instructions more flexible and let the model handle the details naturally.


# End Node
Source: https://docs.retellai.com/build/conversation-flow/end-node



End node is used to end the call. It does not have any edges. The call is ended the moment the agent enters this node.

You can create multiple end nodes within a single agent.

<img />

## Node Settings

* **Speak During Execution**: when enabled, a text input box will show up where you can write instructions for the agent to follow to generate an utterance like `Goodbye, have a nice day` to say while the function is being executed. You can choose between `Prompt` and `Static Sentence`.
* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)


# Extract Dynamic Variable Node
Source: https://docs.retellai.com/build/conversation-flow/extract-dv-node



Extract dynamic variable node is used to extract information from conversation and store them as dynamic variable. It's not intended for having a conversation with the user.

<Frame>
  <img />
</Frame>

## Add a variable

To create a variable, fill in the following details:

* **Variable Name** – A short name to reference this variable.
* **Description** – A brief explanation of what this value should be.
* **Variable Type** – Choose from `Text`, `Number`, `Enum`, or `Boolean`.
* **Enum Options** - Options to choose from. Only when type is enum

***

## Variable Types

You can create variables of the following types:

* **Text** - Any word or sentence. Examples: `"headache"`, `"John Smith"`
* **Number** - A numeric value. Examples: `42`, `98.6`
* **Enum** - A value from a predefined list. Examples: `"Yes"`, `"No"`, `"Maybe"`
* **Boolean** - True or false.

<Frame>
  <img />
</Frame>

## Node Settings

* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **LLM**: choose a different model for this particular node. Will be used for function argument generation, and potentially speak during execution message generation.
* **Fine-tuning Examples**: Can finetune transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)


# Finetune Examples
Source: https://docs.retellai.com/build/conversation-flow/finetune-examples



When agent response or transition is not meeting your expectation, you might want to supply some examples to finetune the behavior. You can do so by adding `finetune examples`.

Here are the nodes that support finetune examples:

* Conversation Node: support finetune examples for response and transition
* Subagent Node: support finetune examples for response and transition
* Function Node: support finetune examples for transition

When configuring the finetune example, you will provide a transcript as the context. You can select `user`, `agent`, `function` as the role of the transcript. When selecting `function` as the role, you can fill out both the invocation and result of the function. Refer to the History tab of the dashboard to see examples of transcripts.

## Finetune Examples for Conversation

<img />

Supplying a transcript as the context is everything you need to do. It's not necessary to provide the entire call transcript, you can simply provide the relevant part. Please note that at least one `agent` response is required, as this is finetuning agent's response.

## Finetune Examples for Transition

<img />

Here you need to provide both a transcript as context, and the transition result. If you cannot distinguish between the different nodes available as transition target, you can try to rename your nodes to make it easier to distinguish.


# Flex Mode
Source: https://docs.retellai.com/build/conversation-flow/flex-mode

Combine conversation flow structure with single prompt flexibility for dynamic task handling

Flex Mode combines the best of both worlds:

* Conversation Flow: clear, visual business logic that’s easy to manage.
* Single Prompt Agent: flexible, natural handling of varied user behavior.

You design your conversation flow as usual (nodes, edges, tools). At
runtime, Flex Mode compiles that flow into one structured prompt made of Tasks
and available Tools. The agent then navigates Tasks dynamically while still
following your global prompt.

## Cost Impact

<Warning>
  Flex mode can significantly increase your LLM costs. Because all node instructions,
  transitions, and tool descriptions are compiled into a single prompt, the total token
  count is much higher than in rigid mode (where only the active node's prompt is sent
  to the LLM). When the combined prompt exceeds 3,500 tokens, the
  [token scaling billing rule](/accounts/billing-exceptions#rule-2-llm-price-scaling-for--3500-token-prompt-length)
  applies, which can multiply your costs several times over.
</Warning>

To control costs, consider using **rigid mode** or **breaking your flow into smaller
components** so that fewer nodes are compiled into a single prompt. If you do use flex
mode, keep node instructions concise to minimize token usage.

## When To Use

* You want the clarity of a flowchart (business steps) but need the freedom of a
  single prompt:
  * You can easily switch context from different tasks e.g. every node would
    become global node
  * Could move on to the proper task if the user completed multiple tasks at the
    same time.
  * After swtich the context to another flow, agent could resume on the previous
    task without repeating the already completed steps.

## How It Works

You can enable the 'Flex Mode' either at Component level or the Agent level.

<Frame>
  <img />
</Frame>

When enabled at agent level, all the nodes get converted to a single flex
node. It will stay on the flex node and behave like a single prompt agent until
reach the 'End Call'.

When enabled on a component, only that component’s nodes are converted into a
single prompt; the rest stays as standard conversation flow.

## Tool Call / Function

The are some differences how flex mode (single prompt) and traditional
conversation flow handle the tool call/function.

* **Speak During Execution** The exection message part will still work the same.
* **Speak After Execution** There is no 'Speak After Execution' setting in Flex
  Mode. The agent will always speak after function execution.
* **Wait For Result** There is no 'waitForResult' setting in Flex Mode. Agent
  will always wait for the function to complete (similar to Single Prompt
  agent).

## Knowledge Base

Node-level knowledge base will be ignored in Flex Mode. You will need to configure the knowledge base at agent level.

## Best Practices & Known Issues

* Write the node instruction in a concise manner so that LLM could better focus
  on the task.
* Only use Prompt edge, avoid using Equation edge as LLM is really bad at
  interpret equation conditions. You might see very weird behaviors.
* Be explicit on transitions: write crisp, observable conditions.
* If you use flex mode for more than 20 nodes, performance might degrade and
  agent might have higher hallucination risk. We recommend splitting into
  smaller components.
* LLM might not always follow the static text instruction.


# Function Node Overview
Source: https://docs.retellai.com/build/conversation-flow/function-node



Function node is used to call a function, whether it's a pre-built function or a custom function. It's not intended for having a conversation with the user, but agent can still talk while in this node if needed.

The function that associates with this node will be called when entering this node.

<img />

## Add a Function

Here you need to add the function first, and then select it inside the node. This way if you delete the node, you don't need to re-create the function again.

<img />

For specific instructions on different types of functions:

* [Custom Function](/build/conversation-flow/custom-function)
* Pre-built Functions:
  * [Check Calendar Availability](/build/check-availability)
  * [Book Calendar](/build/book-calendar)

## When Can Transition Happen

* if `wait for result` is turned off
  * if `speak during execution` is turned on, the agent will transition once done talking
  * if `speak during execution` is turned off, the agent will transition immediately after function gets invoked, which is right upon entering the node
  * if the user interrupts the agent, the transition can also happen once user is done speaking
* if `wait for result` is turned on
  * if `speak during execution` is turned on, the agent will transition once function result is ready and agent is done talking
  * if `speak during execution` is turned off, the agent will transition once function result is ready
  * if the user interrupts the agent, the transition can also happen once function result is ready and user is done speaking

Given that the function node takes function result into consideration for transition timing, you can write your transition condition to be based on the function result.

## Node Settings

* **Speak During Execution**: when enabled, a text input box will show up where you can write instructions for the agent to follow to generate an utterance like `Let me check that for you.` to say while the function is being executed. You can choose between `Prompt` and `Static Sentence`.
* **Wait for Result**: when enabled, the agent will wait for the function to finish executing before attempting to transition to any other node. This guarantees that when you reach the next node, the result is already ready to be used.
* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **Block Interruptions**: when enabled, the agent will not be interrupted by user when speaking.
* **LLM**: choose a different model for this particular node. Will be used for function argument generation, and potentially speak during execution message generation.
* **Fine-tuning Examples**: Can finetune transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)

## How to Tell User the Result

Since the function node is not intended for having a conversation with the user, you will need to attach a conversation node to the function node to tell the user the result. You can create different conversation nodes for different function results, so that it can engage user in different ways when function result varies.


# Global Node
Source: https://docs.retellai.com/build/conversation-flow/global-node



Global nodes can be transitioned to from anywhere in the conversation flow, making them ideal for handling universal scenarios like user objections (e.g. `I want to talk a human / I need to call back later`). Toggle on `Global Node` in the node settings to enable this.

<img />

## Configure Global Node

Set a condition for when the global node should be transitioned to. In the example above, the condition is `When user indicates this is not a good time to continue` — so whenever the user says something like `I need to call back later`, the agent transitions to this node.

Since a global node can be transitioned to from anywhere, it does not need to be connected to the rest of the graph.

## Global Node Examples

Add example conversations to help the AI better understand when to jump to this global node. Click `+ Add` to create examples that demonstrate scenarios where the global node should or should not be activated.

## Go Back to Previous Node

Enable **Go back to previous node** to let the conversation return to where it left off after the global node is handled. Once enabled, a **Go Back Condition** section appears on the node where you define when the agent should navigate back. In the example above, the condition is `User changed their mind and want to continue the call`.

Go back conditions support both prompt-based and equation-based conditions. You can add multiple conditions and reorder them by dragging.

## Prevent Immediate Re-Trigger

Enable **Prevent Immediate Re-Trigger** to pause the global node for a specified number of node steps after it has been triggered. Set the number of **Node steps** (defaults to 3) during which the global node will not be activated again. This prevents the conversation from looping when the user's phrasing keeps matching the global node condition.


# Step 1: Configure global settings
Source: https://docs.retellai.com/build/conversation-flow/global-setting



## Agent Global Settings

Click on empty canvas and click setting to access global setting. Here's where you set a lot of agent level settings.

<Steps>
  <Step title="Configure Voice Settings">
    1. Open the voice selection dropdown menu:

    <img />

    2. Listen to the available voice samples and select the voice you want to use for the agent:

    <img />

    **Custom Voices**: You can also add voices from the ElevenLabs community or clone voices by clicking "Add custom voice". Learn more in our [voice configuration guide](/build/voice).

    3. You can also adjust a couple voice settings:
       * voice temperature to make the voice more variant or stable.
       * voice speed to make the agent speak faster or slower.
       * voice volume to make the agent speak louder or quieter.
       * voice model (if applicable): when using certain voice providers, you can choose between different models that support. Check out dashboard for detailed nuances of each models.
  </Step>

  <Step title="Select Language of Agent">
    Pick the language(s) the agent will understand and speak. This affects speech recognition, voice pronunciation, and the language the agent responds in — you do not need to add a "respond in X" instruction to your prompt.

    To support multiple languages, switch the selector to **Multiselect** and pick the specific languages you want; for best accuracy, prefer a single language when possible. See [Set language for your agent](/agent/language) and [Configure a multilingual agent](/agent/multilingual) for details.
  </Step>

  <Step title="Select a Language Model">
    Select the model you want to use for the agent. Please note that you can override this within individual nodes. Optionally you can tune the LLM temperature to make answers more variant or more stable.

    We recommend starting with GPT-4.1, which offers an optimal balance of:

    * Response quality
    * Latency
    * Cost-effectiveness

    <img />
  </Step>

  <Step title="Write Global Prompt">
    Here's where you specify the agent's persona, identity, guardrails, etc. This set of text will be available in every node, and will influence all response generation.
  </Step>

  <Step title="Configure Knowledge Base">
    Here's where you can supply contexts to agent via documents, urls, texts. Read more at [Knowledge Base Guide](/build/knowledge-base).
  </Step>

  <Step title="Configure Speech Settings">
    Here's a lot of options that allow you to finetune how your agent interacts with user.

    * Background sound: select a background sound that plays throughout the whole call to mimic an environment like call center, making the conversation more humanlike and engaging.
    * Responsiveness: how responsive the agent is. Set it lower if you want agent to respond slower, which can be useful when talking to folks like elderly. Reducing responsiveness by 0.1 adds 0.5 seconds of agent wait time.
    * Interruption Sensitivity: how fast the agent gets interrupted by user interruptions. Set it lower if you want agent to be more resilient to background speech or user interruptions.
    * Backchanneling: Set up how often and what words the agent uses to acknowledge users.
    * Boosted Keywords: Provides some biases towards certain words, making it easier to get recognized. Common ones are brand names, people's names, etc.
    * Speech Normalization: convert entities like date, currency, numbers into plain words, which can help prevent issues where audio generated was not pronouncing those right.
    * Reminder frequency: how often the agent will remind the user when user is inactive.
    * Pronunciation: set up pronunciation guide for specific words.
  </Step>

  <Step title="Configure Call Settings">
    Here's a couple of settings that's more call operation related.

    * Voicemail related settings: set up voicemail detection and what to do when voicemail is detected. See more at [Handle Voicemail](/build/handle-voicemail).
    * End call on silence: set up if user is active for a certain amount of time, the call will be ended.
    * Call duration: set up maximum duration of the call.
    * Pause before speaking: For the beginning of the call, if agent speaks first, it will wait for the configured duration before speaking, useful to handle scenarios when user is still picking up the phone.
  </Step>

  <Step title="Configure Post Call Analysis">
    Probably set up later, read more at [Post Call Analysis Guide](/features/post-call-analysis-overview).
  </Step>

  <Step title="Configure Privacy & Webhook">
    Here's where you can set up whether to opt out sensitive data storage, and configure webhook settings for receiving call related events.
  </Step>
</Steps>

## Configure Who Speaks First

Click on `begin` icon, and you can select who speaks first in the call.

<img />


# Logic Split Node
Source: https://docs.retellai.com/build/conversation-flow/logic-split-node



Logic split node is used to branch out the conversation flow based on the conditions. When entering this node, the agent will immediately evaluate the conditions and branch out to the corresponding destination nodes. The agent would not speak in this node, and the time spent in this node is minimal.

It can come in handy when you want to further split the conversation flow based on the conditions, and do not want to stack all your conditions in previous nodes. It can also be hard for agent to handle a bunch of conditions all at once, so this node can help break it down. It can also be useful when you want to branch out based on dynamic variables.

<img />

## When Can Transition Happen

Transition happens immediately when agent enters this node.

## Configure branching logic

* add conditions just like you would in other nodes
* setup the else destination: there will always be an else condition, which will be the default destination if none of the conditions are met, because this node is designed to be a split point and you want to make sure the conversation flow is not stuck here.

## Rest of Node Settings

* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **Fine-tuning Examples**: Can finetune transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)


# MCP Node
Source: https://docs.retellai.com/build/conversation-flow/mcp-node



MCP node is used to call tools on your MCP server.  It's not intended for having a conversation with the user, but agent can still talk while in this node if needed.

<Frame>
  <img />
</Frame>

## Add MCP server

<Steps>
  <Step title="Add MCP server">
    To create a MCP node, we first need to add MCP server.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set request headers (optional)">
    You can define custom headers to include with the request Retell sends to your MCP Server.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set query parameters (optional)">
    You can define query parameters to include in the request URL that Retell appends to your MCP Server Endpoint.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Add MCP Tool">
    Select MCP Tool

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set response variables (optional)">
    Extract values from the MCP tool response and save them as <strong>dynamic variables</strong> for use later in the conversation.

    For example, you can extract a user’s name from the response and reference it later using <code>\{\{user\_name}}</code>.

    Example response body

    ```javascript theme={null}
    {
    "properties": {
        "user": {
        "name": "John Doe",
        "age": 26
        }
    }
    }
    ```

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>

## Node Settings

* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **Fine-tuning Examples**: Can finetune transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)


# Node Overview
Source: https://docs.retellai.com/build/conversation-flow/node

Understanding nodes - the building blocks of conversation flow agents

## What are Nodes?

Nodes are the fundamental building blocks of your conversation flow. Each node represents a specific step or action in your agent's conversation, with its own logic, behavior, and purpose.

### Key Concepts

* **Node Type**: Determines the node's functionality (conversation, subagent, function call, logic, etc.)
* **Edges**: Connections between nodes that define the conversation flow
* **Transition Conditions**: Rules that determine when and where to move next
* **Fine-tuning**: Each node can be optimized independently for better performance

### Why Use Nodes?

By breaking complex workflows into individual nodes:

* **Precise Control**: Define exact behavior for each conversation scenario
* **Better Performance**: Fine-tune specific parts without affecting others
* **Easier Debugging**: Isolate and fix issues in specific conversation paths
* **Reusability**: Connect nodes in different ways for various flows

## Node Types Available

### Conversation Nodes

* [**Conversation Node**](/build/conversation-flow/conversation-node): Handle dialogue and user interactions without tool calling
* [**Subagent Node**](/build/conversation-flow/subagent-node): Handle dialogue and user interactions with tool calling
* [**Extract DV Node**](/build/conversation-flow/extract-dv-node): Extract and store dynamic variables from conversations

### Action Nodes

* [**Function Node**](/build/conversation-flow/function-node): Execute custom functions and API calls
* [**Code Node**](/build/conversation-flow/code-node): Execute JavaScript code directly without an external server
* [**SMS Node**](/build/conversation-flow/sms-node): Send SMS messages during the call
* [**MCP Node**](/build/conversation-flow/mcp-node): Integrate with Model Context Protocol tools

### Call Control Nodes

* [**Call Transfer Node**](/build/conversation-flow/call-transfer-node): Transfer calls to other phone numbers
* [**Transfer Agent Node**](/build/conversation-flow/transfer-agent-node): Transfer to another Retell agent
* [**Press Digit Node**](/build/conversation-flow/press-digit-node): Send DTMF tones (press digits)
* [**End Node**](/build/conversation-flow/end-node): Terminate the call gracefully

### Logic Nodes

* [**Logic Split Node**](/build/conversation-flow/logic-split-node): Create conditional branches based on variables

## Add a Node

<Steps>
  <Step title="Select node type">
    Click from the left sidebar to select the node type you want to add. Click on it, and it will be added to the canvas.

    <Frame>
      <img alt="Left sidebar showing available node types to add to the conversation flow" />
    </Frame>
  </Step>

  <Step title="Configure the node">
    Configure the node by clicking on the node, check the setting on the right, and fill in node instructions inside the node. Check out respective node guide for more details.

    <Frame>
      <img alt="Node configuration panel on the right showing settings and instructions" />
    </Frame>
  </Step>

  <Step title="Add transition conditions as needed">
    Add edges by clicking on bottom part of the node, and add your transition conditions. Check out next step for more details on how to add transition conditions.
  </Step>

  <Step title="Connect node">
    Click and hold the circle to start a line that connects the node to other node, and other node to this node.

    <Frame>
      <img alt="Connecting nodes by dragging from the circle connector to create edges" />
    </Frame>
  </Step>
</Steps>

## Organize Nodes

Sometimes after adding a great amount of nodes, the canvas can get cluttered. You can use the `Organize` button to automatically organize the nodes.

<Frame>
  <img alt="Organize button that automatically arranges nodes for better visibility" />
</Frame>

## FAQ

<AccordionGroup>
  <Accordion title="When should I break down a node?">
    Consider breaking down a node when:

    * The node handles multiple complex logic paths
    * The LLM struggles with consistency (hallucinations or incorrect responses)
    * You need different settings (model, temperature) for different parts
    * The conversation flow becomes hard to follow or debug

    Breaking complex nodes into smaller, focused nodes often improves reliability.
  </Accordion>

  <Accordion title="How to zoom in and out the canvas?">
    Depending on whether you are using mouse or touchpad, you can use the scroll wheel or pinch to zoom.
  </Accordion>

  <Accordion title="Is there a limit on the number of nodes?">
    No, you can add as many nodes as you want.
  </Accordion>
</AccordionGroup>


# Conversation Flow Overview
Source: https://docs.retellai.com/build/conversation-flow/overview

Learn how to build structured conversational agents using nodes and transitions for complex call scenarios

## What is a Conversation Flow Agent?

Conversation flow agents allow you to create multiple nodes to handle different scenarios in conversations. This approach provides more fine-grained control over the conversation flow compared to Single/Multi Prompt agents, enabling you to handle more complex scenarios with predictable outcomes.

### Key Benefits

* **Structured conversations**: Define exact paths and transitions
* **Predictable behavior**: Each node has specific logic and outcomes
* **Complex scenario handling**: Support for conditional branching and state management
* **Fine-tuning capabilities**: Improve performance with node-specific examples

<Frame>
  <img alt="Conversation flow diagram showing nodes connected by edges with transition conditions" />
</Frame>

## Components

* **Global Settings**: Configuration that applies to the entire conversation, including:
  * Global prompt and personality
  * Default voice and language settings
  * Agent-wide parameters and behaviors

* **Node**: The basic unit of conversation flow. Multiple node types are available:
  * Conversation nodes for dialogue without tool calling
  * Subagent nodes for dialogue with tool calling
  * Function nodes for deterministic API and tool execution
  * Logic nodes for branching
  * End nodes for call termination

* **Edge**: Connections between nodes that define transition logic:
  * Condition-based transitions
  * Default fallback paths
  * Dynamic routing based on conversation context

* **Tools / Functions**: Reusable capabilities that can be attached to subagent nodes or invoked from function nodes. Conversation nodes do not use tools / functions:
  * Custom API integrations
  * Built-in utilities (calendar, SMS, transfers)
  * External service connections

## How it Works

Every node defines a small set of logic, and the transition condition is used to determine which node to transition to. Once the condition is met when checked, the agent will transition to the next node. There are also finetune examples on nodes that can help you further improve the performance. It might take longer to set up, as you want to cover all the scenarios, but after that it's much easier to maintain and the performance is more stable and predictable.

## Quickstart

Head to the Dashboard, create a new conversation flow agent and select a pre-built template to get started. You can view all options available to the agent within the Dashboard, with details of the options and any latency implications listed there. You can also view the estimated latency and cost of the agent. Modify the template to your needs, all changes are auto-saved.

## Pricing

Since the choice of model can be overridden within individual nodes, the pricing for each call is calculated based on:

* Time spent in each node (seconds)
* Model price per second for that specific node
* Total aggregated across all nodes visited during the call

This allows you to optimize costs by using different models for different parts of the conversation (e.g., cheaper models for simple routing, premium models for complex interactions).


# Press Digit Node
Source: https://docs.retellai.com/build/conversation-flow/press-digit-node



The Press Digit Node is used to navigate through IVR (Interactive Voice Response) systems. When in this node, the agent will not speak. Instead, it evaluates whether it should press a digit and determines which specific digit to press.

The node evaluates whether to press a digit each time the user (IVR system) finishes speaking. This timing is also affected by the detection delay setting. If a digit press is needed, the agent will infer the appropriate digit and press it.

<img alt="Press digit node navigating an IVR system" />

## Configure Press Digit Behavior

<Steps>
  <Step title="Setup IVR Navigation Instructions">
    Provide clear instructions so the agent knows whether and what digit to press. Include keywords or phrases to listen for, as well as which ones to avoid.

    **Sample prompt:**

    ```
     Your goal is to reach the scheduling or appointments department.

     Preferred navigation keywords:
     • Scheduling
     • Appointments
     • New patients
     • Front desk

     Avoid:
     • Billing
     • Referrals
     • Medical records
     • Clinical departments

     If you are unsure which IVR option is correct:
     Choose the option most closely related to scheduling or appointments.
    ```
  </Step>

  <Step title="Configure Detection Delay">
    Some IVR systems speak slowly, so to make sure the agent does not make any decision prematurely, you can set a delay on pauses to make sure the whole IVR menu is captured. We recommend setting this to 1 second.
  </Step>

  <Step title="Configure Transitions">
    Transitions occur when the IVR system finishes speaking. When writing your transitions, ensure you cover both successful navigation and potential failure scenarios or edge cases.

    **Success scenario:** Define when the agent has successfully navigated to the target. For example, write conditions like `Reached scheduling department`. If the digit press was correct, the IVR response will confirm this.

    **Edge cases:** Cover scenarios like getting stuck in loops. For example, write conditions like `Menu repeated 3 times` to handle repetitive menus.

    **Example transition conditions:**

    ```
    You've reached the scheduling department.
    ```

    ```
    Menu repeated 3 times.
    ```

    ```
    You've reached the wrong department or company.
    ```

    ```
    You've reached an after-hours or voicemail message.
    ```
  </Step>
</Steps>

## Rest of Node Settings

* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **LLM**: choose a different model for this particular node. Will be used for determining whether and what digit to press.


# SMS Node
Source: https://docs.retellai.com/build/conversation-flow/sms-node



SMS node is used to send an SMS during a phone call. You can send to the caller's number or a different number.

<Note> This node only works for phone numbers that have SMS enabled, or when using an SMS-approved Retell number. Read more about [enabling SMS](/deploy/enable-sms). </Note>

The SMS will be sent when entering this node.

## Choose where to send from

You can choose one of two options for the sending number:

* **SMS-approved Retell number**: Send from Retell's pool of numbers that are already approved for SMS. This bypasses the A2P application process entirely. The message content is a **preset template provided by Retell** — you cannot customize the text or use a prompt.
* **Agent's associated number**: Send from the phone number bound to the agent. This requires your number to have SMS enabled through the [A2P application](/deploy/enable-sms#enable-sms-capabilities).

<Frame>
  <img alt="In-Call SMS node showing fixed text content and transition edges" />
</Frame>

<Tip>Agents can also **receive SMS during an active call** and understand the content, including text, images, audio, and video. This works out of the box for Retell Twilio numbers, and for custom telephony numbers that passed A2P applications. Read more at [Receive SMS during call](/deploy/enable-sms#receive-sms-during-call).</Tip>

## Configure SMS content

* **When sending from the agent's associated number**: You can write a prompt to let the agent infer the SMS content, or use static SMS content. Dynamic variables are supported for static SMS content.
* **When sending from an SMS-approved Retell number**: The message is a preset template provided by Retell. You cannot edit the content.

## Configure SMS destination

By default, the SMS is sent to the caller's number. You can also choose to send to a different number — either a static number or a dynamic variable (e.g. `{{customer_phone}}`).

## When Can Transition Happen

The node would transition to the next node once the SMS is successfully sent or failed to send. It should take less than 2 seconds to get that result. It will transition out of the node purely based on the SMS result.

## Node Settings

* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **LLM**: choose a different model for this particular node. Will be used for function argument generation, and potentially speak during execution message generation.


# Subagent Node
Source: https://docs.retellai.com/build/conversation-flow/subagent-node

Use a subagent node for dialogue that can call tools during the conversation

Subagent node is used to have a conversation with the user while allowing the agent to call tools / functions during the conversation. Use it when the agent should decide whether and when to use a tool / function based on the conversation context.

If you only need dialogue without tool calling, use a [Conversation Node](/build/conversation-flow/conversation-node).

## How It Works

When a subagent node has tools / functions attached, the LLM receives both the node instruction and the list of available tools / functions. During the conversation, the LLM determines when a tool / function should be called based on context, extracts the required parameters, and invokes it while maintaining the dialogue with the user.

* Multiple tools / functions can be added to a single subagent node
* The agent can continue talking while a tool / function executes
* Tool / function results are available to the LLM for generating follow-up responses

## Write Instruction

Subagent nodes only support `Prompt` instructions. Unlike a conversation node, `Static Sentence` is not supported.

Write the instruction to define the task, what information the agent should gather, and when it should use the available tools / functions.

For example:

```text theme={null}
Help the user check their order status. If the user provides an order number,
use the available order lookup tool to retrieve the latest status.
```

## Subagent Node vs Function Node

Subagent nodes and [function nodes](/build/conversation-flow/function-node) serve different purposes:

|                    | Function Node                                                  | Subagent Node                                                                           |
| ------------------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Execution**      | Deterministic — executes on node entry                         | LLM-driven — called when the LLM decides it's appropriate                               |
| **Tools per node** | One                                                            | Multiple                                                                                |
| **Conversation**   | Not intended for dialogue                                      | Full dialogue with tools available                                                      |
| **Best for**       | Always-execute actions (e.g. always look up an order on entry) | Context-dependent actions during dialogue (e.g. look up an order only if the user asks) |

**Use function nodes** when you want guaranteed execution every time the flow reaches that step.

**Use subagent nodes** when the agent should decide whether and when to call a tool / function based on what the user says.

## Add Tools / Functions

<Steps>
  <Step title="Select a subagent node">
    Click on a subagent node to open its settings panel on the right side.
  </Step>

  <Step title="Add a tool / function">
    In the settings panel, find the **Tools** section and click **+ Add**.

    Select the tool / function type from the dropdown menu.
  </Step>

  <Step title="Configure the tool / function">
    Configure the tool / function based on its type. See the **Available Tool / Function Types** table below for configuration details for each type.
  </Step>

  <Step title="Update the node instruction">
    Update the node prompt to guide the LLM on when to use the tool / function.
  </Step>
</Steps>

## Available Tool / Function Types

| Tool Type                   | Description                                             | Configuration Guide                                               |
| --------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------- |
| Custom Function             | Make HTTP requests to your external APIs                | [Custom Function](/build/conversation-flow/custom-function)       |
| Code Tool                   | Run JavaScript code directly without an external server | [Code Tool](/build/single-multi-prompt/code-tool)                 |
| Check Calendar Availability | Query available time slots via Cal.com                  | [Check Availability](/build/check-availability)                   |
| Book Appointment            | Book calendar events via Cal.com                        | [Book Calendar](/build/book-calendar)                             |
| End Call                    | Terminate the call                                      | [End Call](/build/single-multi-prompt/end-call)                   |
| Transfer Call               | Transfer to a phone number                              | [Transfer Call](/build/single-multi-prompt/transfer-call)         |
| Transfer Agent              | Transfer to another Retell agent                        | [Transfer Agent](/build/single-multi-prompt/transfer-agent)       |
| Press Digit                 | Send DTMF tones                                         | [Press Digit](/build/single-multi-prompt/press-digit)             |
| Send SMS                    | Send a text message                                     | [Send SMS](/build/single-multi-prompt/send-sms)                   |
| Extract Dynamic Variable    | Extract variables from the conversation                 | [Extract Dynamic Variable](/build/single-multi-prompt/extract-dv) |
| MCP Tool                    | Call tools on your MCP server                           | [MCP Node](/build/conversation-flow/mcp-node)                     |

## Execution Speech Settings

Each tool / function has settings that control what the agent says while it is running and after it completes.

### Speak During Execution

When enabled, the agent says a message while the tool / function is executing, for example `One moment, let me check that for you.` This is recommended when the tool / function takes over 1 second, including network latency, so the agent remains responsive.

You can configure how the message is generated:

* **Prompt**: The LLM dynamically generates what to say based on a description you provide.
* **Static Sentence**: The agent speaks the exact text you provide.

### Speak After Execution

When enabled, the agent calls the LLM after the tool / function returns a result so it can speak about the outcome to the user. Turn this off if you want to run it silently.

<Note>
  * **Speak During Execution** is available on: Custom Function, Code Tool, End Call, Transfer Call, Transfer Agent, and MCP Tool.
  * **Speak After Execution** is available on: Custom Function, Code Tool, and MCP Tool.
</Note>

## When Can Transition Happen

* when user is done speaking
* when `Skip Response` is enabled and agent finishes speaking

Tool / function execution happens within the subagent node, so the node can stay active across multiple turns and tool / function calls before it transitions.

## Node Settings

* **Tools**: attach the tools / functions this subagent can use during the conversation.
* **Skip Response**: when enabled, the transition will only have one edge that you can connect, and when agent is done talking, it will transition to the next node via that specific edge.
* **Knowledge Base**: configure node-level knowledge bases to combine topic-specific knowledge with the agent-level knowledge base. Read more at [Knowledge Base](/build/knowledge-base).
* **Global Node**: read more at [Global Node](/build/conversation-flow/global-node)
* **Block Interruptions**: when enabled, the agent will not be interrupted by user when speaking.
* **LLM**: choose a different model for this particular node. Will be used for response generation, tool / function selection, and tool / function argument generation.
* **Fine-tuning Examples**: Can finetune conversation response, and transition. Read more at [Finetune Examples](/build/conversation-flow/finetune-examples)

## Best Practices

* **Be explicit in your node instruction.** Tell the agent when each tool / function should be used.
* **Use function nodes for guaranteed execution.** If a tool / function must always run at a certain point in the flow, use a function node instead.
* **Avoid adding too many tools / functions to one subagent node.** If you have many tools / functions, consider splitting them across multiple subagent nodes.


# Agent Transfer Node
Source: https://docs.retellai.com/build/conversation-flow/transfer-agent-node



In advanced call flows, it's common to switch the handling agent, transferring the conversation from one AI agent to another. **Agent Transfer** (also known as **Agent Swap**) enables you to modularize tasks and re-use specialized agents without relying on [traditional phone-based transfers](/build/single-multi-prompt/transfer-call). Examples include:

* Transferring from a front-desk agent to an appointment-booking agent based on task.
* Transferring from an agent speaking one language to another agent handling a different language, based on user preference.

## Why Use Agent Transfer Instead of Call Transfer?

Compared to transferring to another agent using [transfer call](/build/conversation-flow/call-transfer-node), **Agent Transfer** offers significant advantages:

* **Lower Latency**: The transition between agents is near-instant, much lower than transfer call.
* **Better Reliability**: No need to create a new phone call, avoiding potential telephony failures.
* **No Handoff Message Needed**: The destination agent has access to the full conversation history, eliminating the need for adding hand-off messages or repeated customer questions.
* **No Separate Numbers for Agents**: Agents receiving transfers don’t need their own phone numbers — one number is all you need, no matter how many agents you transfer to.

## Transfer Settings Behavior

The following settings of the first agent will be used throughout the call:

* optInSignedUrl
* optOutSensitiveDataStorage
* webHookUrl

All other settings — such as language, voice, and voiceModel — will reflect the currently active agent.

## Steps

<Steps>
  <Step title="Add Agent Transfer Node">
    Select "Agent Transfer" from the 'Add New Node' menu.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Details">
    You can configure the following main settings:

    * **Transfer agent**: the ID and version of a specific agent to transfer to. You can select the latest version as well.
    * **Speak during execution and messages**: if the agent should speak something while performing the transfer.
    * **Post call analysis setting**: for post-call analysis, only extract dynamic variables for the transferred agent, or both agents.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Test and Debug">
    You can test agent transfer both in web call and playground.

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>


# Step 3: Add transition conditions
Source: https://docs.retellai.com/build/conversation-flow/transition-condition



## What is a transition condition?

Transition conditions are used to determine whether and which node the agent will transition to. If no transition condition is met, the agent will transition to the next node. This is the most essential part of the conversation flow, as this gives you the utmost control, and this requires most careful testing.

## Types of transition conditions

There are two types of transition conditions:

* **Prompt**: The condition is a prompt that is evaluated by the LLM.
* **Equation**: The condition is a mathematical equation that is hardcoded. This is useful for testing if dynamic variables meet a certain condition.

All equation conditions are evaluated first, and then the prompt conditions are evaluated. Note that equation conditions are evaluated from top to bottom, and we travel on the first condition that evaluates to true.

Example of prompt conditions:

* `User said something about booking a meeting`
* `User said something about cancelling a meeting`
* `User claims to be over 18`
* `User said they lived in New York`
* `User said they lived in New York or Los Angeles`

Example of equation conditions:

```
- {{user_age}} > 18
- {{current_time}} > 9 AND {{current_time}} < 18
- {{user_location}} == "New York"
- {{user_location}} != "New York"
- "New York, Los Angeles" CONTAINS {{user_location}}
- "New York, Los Angeles" NOT CONTAINS {{user_location}}
- {{user_age}} < 18 OR {{user_location}} == "New York"
- {{name}} exists
```

Note: You can only use variables that are passed in as dynamic variables for equation conditions. If you need to use information extracted by the LLM (such as information learned during the call), you can use prompt conditions.

## Where to define transition conditions?

For different node types:

* Conversation & Function & Press Digit Node: can define conditions to transition out of the node.
* Call Transfer Node: can select a destination node to transition to when transfer is unsuccessful.

For features:

* Skip response: can select a destination node to transition to when agent done speaking content of that node.
* [Global node](/build/conversation-flow/global-node): When enabled, must define the condition to transition into this node.

## How to update transition conditions?

You can update transition conditions by clicking on the node and then clicking on the "+" button for adding a transition condition.
You can then choose to add either a prompt or an equation transition condition. See the picture below.

<img />

For prompt conditions, this will open the text on the transition condition editing.

For equation conditions, this will open the equation editor. See the picture below.

<img />

This editor allows you to add and drop equations. You can click on the "Add equation" button to add a new equation.
You can delete an equation by clicking on the trash can icon. In addition, you can change the "ANY" to "ALL" to force all equations to be true instead of just one.

To change the order of the equations, you can click on the 6 dots on the left of the equation and drag it up or down. See the picture below.

<img />

## New equation conditions

### Check Dynamic variable exists

You can check whether a dynamic variable exists or doesn't exist using the following equation conditions:

* `{{variable_name}} exists` - Returns true if the variable is defined and has a value (even an empty string is considered having a value)
* `{{variable_name}} does not exists` - Returns true if the variable is undefined

This is particularly useful when you want to handle cases where certain information may or may not be available. For example:

```
- {{user_email}} exists
- {{user_phone}} not exists
- {{preferred_language}} exists
```

<img />

## When will the transition happen?

It usually happens after user speaks, but also have other cases based on node type. Check out specific docs for that node to learn more.

When you are testing in the dashboard (both audio and text), you can see what node is highlighted to find the current node, so you can see how and when the transition happens.

## What should I write inside the transition condition?

Although the agent will have access to the current node's instruction when evaluating the conditions, it's recommended to write conditions to be clear and not reference on the instruction that much.

Here're some examples:

* `When user indicates they want to book a meeting`
* `User declines the invitation`
* `User responds to question of their age`
* example for function nodes where you can reference function results: `CRM lookup returned successful result`

To ensure a smooth transition (making sure your agent does not get stuck on a node), it's recommended to cover all possible cases inside transition condition. Some general cases can be covered by the global nodes (like objection handling), so you can focus on the specific cases that can happen inside the specific node.

For equation conditions, it's recommended to cover all branching paths that are determined solely by the dynamic variables.
This can be done if we want to treat users in California and New York differently, and we have access to the user's location before the call starts.
In this case, the equation conditions can be:

```
- {{user_location}} == "New York"
- {{user_location}} == "Los Angeles"
```

Note that the ==, Contains, Not Contains, and Not Equal are string comparisons. They do not require numerical input.
The other comparison operators require numerical input, and will always evaluate to false if the input is not a number.

## Improve transition condition

If you've observed an incorrect transition, you can

* prompt engineer the conditions
* add transition finetune examples (read more at [Finetune Examples](/build/conversation-flow/finetune-examples))

## FAQ

<AccordionGroup>
  <Accordion title="User said something totally unrelated to the transition condition, what would happen?">
    If what user said can be handled by a global node, the agent will transition to the global node. Otherwise the agent will stay in the current node.
  </Accordion>

  <Accordion title="How to see the transition for a past call?">
    You can find node transitions inside the call transcript in the history tab, it will show the node names that it transitions from and to. Thus you might want to name your nodes accordingly.
  </Accordion>

  <Accordion title="Is there a limit on the number of transition conditions?">
    No, but more conditions can make it harder for agent to choose the desired one.
  </Accordion>
</AccordionGroup>


# Create chat agent
Source: https://docs.retellai.com/build/create-chat-agent

Learn how to create and configure a chat agent in Retell

This guide explains how to create and configure a chat agent in Retell. Chat agents allow you to implement conversational AI experiences through text-based interfaces.

**Note:** Retell does not provide native integration with SMS or chat applications at this moment. You can only interact with the chat agent via API.

## Creating a Chat Agent

You have two options:

### Create a New Chat Agent

1. Navigate to the Agents section in your Retell dashboard
2. Click "Create New Agent"
3. Select "Chat Agent" as the agent type
4. Configure your agent settings and prompts

<Frame>
  <img alt="Create a New Chat Agent" />
</Frame>

### Convert an Existing Voice Agent

1. Open an existing voice agent
2. Click "Convert to Chat Agent"
3. Review the conversion warnings

<Frame>
  <img alt="Convert an Existing Voice Agent" />
</Frame>

**Note:** Chat agents do not support certain voice-specific functions like call transfers, DTMF (press digits), or telephony features. During conversion, such nodes or functions will be automatically removed.

## Next Steps

After creating your chat agent, you can:

* [Create a chat session](/api-references/create-chat)
* [Generate responses with chat completion](/deploy/create-chat-completion)


# Dynamic Variables
Source: https://docs.retellai.com/build/dynamic-variables

Learn how to personalize your agent's responses using dynamic variables

## Overview

Dynamic variables allow you to inject personalized data into your agent's responses for each specific call. Using the `{{variable_name}}` syntax, you can create agents that adapt to different contexts while maintaining consistent conversation flows.

### Common Use Cases

* **Personalized greetings**: "Hello `{{customer_name}}`, thanks for calling!"
* **Context-aware responses**: "I see you're calling about order `{{order_id}}`"
* **Dynamic routing**: Transfer to different numbers based on `{{department}}`
* **Time-sensitive information**: Reference `{{appointment_date}}` or `{{deadline}}`

### Where Dynamic Variables Work

Dynamic variables can be used in:

* **Prompts**: Agent instructions and personality
* **Begin message**: Opening greeting
* **Tool configurations**:
  * Custom function URLs
  * Tool descriptions
  * Property descriptions
* **Call handling**:
  * Voicemail prompts and messages
  * Transfer call phone numbers
  * Warm transfer instructions
* Webhook url

## Add & test dynamic variables

<Steps>
  <Step title="Add dynamic variables in your prompts">
    Dynamic variables are placeholders surrounded by double curly braces. For example:

    ```json theme={null}
    "Hello {{user_name}}, I understand you're interested in {{product_name}}. How can I help you today?"
    ```

    Supported fields include a **variable picker** so you do not have to remember exact names:

    1. Type **`{{`** where you want a variable. A dropdown opens listing variables that apply in that context (for example, default system variables plus variables defined for the agent or flow).
    2. **Filter** the list by typing more characters after `{{`.
    3. **Choose a variable** with **Enter**, a **click**, or **Tab**. The editor inserts the full placeholder and closes the braces, for example `{{customer_name}}`.

    <Note>
      You can still type `{{variable_name}}` by hand in supported fields. The picker is optional.
    </Note>
  </Step>

  <Step title="Test your dynamic variables">
    Before deploying, test your dynamic variables using the web interface

    <Frame>
      <img alt="Testing dynamic variables in dashboard" />
    </Frame>
  </Step>

  <Step title="Configure agent-level default dynamic variables">
    You can set default values for dynamic variables at the agent level. Default variables serve as a fallback and will only be used when specific variables aren't included in the call request.

    <Frame>
      <img alt="Default dynamic variable values in agent settings" />
    </Frame>
  </Step>

  <Step title="Implement in production">
    ### For Outbound Calls

    When using the [Create Phone Call](/api-references/create-phone-call) API, set your variables in the
    `retell_llm_dynamic_variables` field. Note that all values must be strings:

    ```json theme={null}
    {
        "user_name": "John Smith",
        "product_name": "Premium Plan",
        "account_status": "active"
    }
    ```

    ### For Inbound Calls

    You can supply dynamic variables in the [Inbound Call Webhook](/features/inbound-call-webhook). More details are at the linked doc.
  </Step>
</Steps>

> **Important:** All values in `retell_llm_dynamic_variables` must be strings. Numbers, booleans, or other data types are
> not supported.

<Note>The spaces around the variable name will be trimmed when evaluating the variable.</Note>

## Default System Variables

Retell automatically provides these system variables - no configuration required:

| Variable                          | Description                                                                                          | Example                                                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `{{current_agent_state}}`         | Current state name (for multi-state agents)                                                          | "greeting"                                                                                                            |
| `{{previous_agent_state}}`        | Previous state name (for multi-state agents)                                                         | "qualification"                                                                                                       |
| `{{current_time}}`                | Current time in `America/Los_Angeles`                                                                | "Thursday, March 28, 2024 at 11:46 PM PST"                                                                            |
| `{{current_time_[timezone]}}`     | Current time in specified `timezone`, for example: `{{current_time_Australia/Sydney}}`               | "Thursday, March 28, 2024 at 11:46 PM AEDT"                                                                           |
| `{{current_hour}}`                | Current hour as a fraction in `America/Los_Angeles`                                                  | "3.5"                                                                                                                 |
| `{{current_hour_[timezone]}}`     | Current hour as a fraction in specified `timezone`, for example: `{{current_hour_Australia/Sydney}}` | "3.5"                                                                                                                 |
| `{{current_calendar}}`            | 14-day calendar in `America/Los_Angeles`                                                             | "Thursday, March 28, 2024 PST (Today)<br />Friday, March 29, 2024 PST<br />...<br />Wednesday, April 10, 2024 PST"    |
| `{{current_calendar_[timezone]}}` | 14-day calendar in specified `timezone`, for example: `{{current_calendar_Australia/Sydney}}`        | "Thursday, March 28, 2024 AEDT (Today)<br />Friday, March 29, 2024 AEDT<br />...<br />Wednesday, April 10, 2024 AEDT" |
| `{{session_type}}`                | Session type, `voice` or `chat`                                                                      | `voice`                                                                                                               |
| `{{session_duration}}`            | How long the session has been running, available after call / chat starts                            | `20 minutes 30 seconds`                                                                                               |

### Phone Call Variables

These variables are only available for phone calls:

| Variable           | Description                                                              | Example                            |
| ------------------ | ------------------------------------------------------------------------ | ---------------------------------- |
| `{{direction}}`    | Call direction, `inbound` or `outbound`                                  | `inbound`                          |
| `{{user_number}}`  | User's phone number (from\_number for inbound, to\_number for outbound)  | `+12137771234`                     |
| `{{agent_number}}` | Agent's phone number (to\_number for inbound, from\_number for outbound) | `+12137771235`                     |
| `{{call_id}}`      | Current call session id                                                  | `call_12345678906eaa0222bd3dd2a6c` |
| `{{call_type}}`    | Call type, `web_call` or `phone_call`                                    | "phone\_call"                      |

### Chat Variables

These variables are only available for chat sessions:

| Variable      | Description                                        | Example                            |
| ------------- | -------------------------------------------------- | ---------------------------------- |
| `{{chat_id}}` | The unique identifier for the current chat session | `chat_12345678906eaa0222bd3dd2a6c` |

## Nested Variables

Retell supports nested variables, you can use the following syntax to create nested variables:

```
{{current_time_{{my_timezone}} }}
```

Now if you have set `my_timezone` to `America/Los_Angeles`, this would evaluate to `{{current_time_America/Los_Angeles }}` first, and will then evaluate to the actual time, as this is a system default variable.

## Handling Missing Variables

### Default Behavior

When a dynamic variable has no assigned value, it remains in its raw form with the curly braces intact:

**Example:**

* Prompt: `"Hello {{user_name}}, how can I help you today?"`
* If `user_name` is not provided: `"Hello {{user_name}}, how can I help you today?"`
* If `user_name` is "John": `"Hello John, how can I help you today?"`

### Checking for Unset Variables

#### In Conversation Flow (Equations)

To check if a variable is set in conversation flow conditions:

```
Equation: {{user_name}} exists
Result: True if variable is defined (even an empty string is considered having a value)
```

#### In Prompts

To handle unset variables in your prompts, you can add conditional logic:

```markdown theme={null}
If {{user_name}} appears with curly braces, use a generic greeting.
Otherwise, greet the customer by name.
```

### Best Practices for Missing Variables

1. **Set defaults at agent level**: Configure fallback values in agent settings
2. **Use defensive prompting**: Design prompts that work with or without variables
3. **Test thoroughly**: Always test with both set and unset variables
4. **Document requirements**: Clearly indicate which variables are required vs optional

## 🎦 Video Tutorial

<iframe title="YouTube video player" />

### Additional Resources

* [Community Templates](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope): Examples and patterns from the Retell community
* [API Reference](/api-references/create-phone-call): Full documentation on passing dynamic variables
* [Inbound Webhook Guide](/features/inbound-call-webhook): Setting variables for incoming calls


# Guardrails
Source: https://docs.retellai.com/build/guardrails

Detect and prevent prohibited topics in agent output and user input using built-in content guardrails.

Guardrails are a built-in content moderation layer that checks agent responses and user messages for prohibited topics. When a guardrail triggers, the prohibited content is automatically replaced with a safe placeholder message, keeping the call going without interruption.

## How Guardrails Work

Guardrails apply in two ways:

* **Output guardrails** check what the agent says. If the agent's response contains a prohibited topic, that response is replaced with a placeholder message before being spoken.
* **Input guardrails** check what the user says. If the user's message contains a prohibited topic, the agent responds with a placeholder message instead of processing the request.

In both cases, the call continues normally after the placeholder is delivered. Guardrails do not end the call, transfer the call, or trigger any other action — they only replace the problematic message.

## Configuring Guardrails

You can configure guardrails when creating or updating an agent, either through the dashboard or the API. In the dashboard, guardrail settings are under **Security & Fallback Settings**.

<Info>
  Guardrails add about 50ms of latency to calls.
</Info>

<Frame>
  <img alt="Main guardrail settings screen showing output and input topic toggles" />
</Frame>

### Output Topics

These categories detect prohibited content in agent responses:

| Topic                           | Description                                               |
| ------------------------------- | --------------------------------------------------------- |
| `harassment`                    | Harassing or abusive language                             |
| `self_harm`                     | Content related to self-harm                              |
| `sexual_exploitation`           | Sexually exploitative content                             |
| `violence`                      | Violent content                                           |
| `defense_and_national_security` | Defense and national security topics                      |
| `illicit_and_harmful_activity`  | Illicit or harmful activities                             |
| `gambling`                      | Gambling-related content                                  |
| `regulated_professional_advice` | Regulated professional advice (legal, medical, financial) |
| `child_safety_and_exploitation` | Child safety and exploitation content                     |

<Frame>
  <img alt="Output guardrail categories for agent responses" />
</Frame>

### Input Topics

One input topic is available; it detects attempts to jailbreak or manipulate the agent.

| Topic                             | Description                                   |
| --------------------------------- | --------------------------------------------- |
| `platform_integrity_jailbreaking` | Attempts to jailbreak or manipulate the agent |

<Frame>
  <img alt="Input guardrail categories for user messages" />
</Frame>


# Handle background speech & noise
Source: https://docs.retellai.com/build/handle-background-noise

Optimize AI agent performance in noisy environments by adjusting interruption sensitivity

In real-world scenarios, phone calls often face audio quality challenges such as background noise, echo, or other unwanted sounds.
We have a couple different features that are designed to help you handle these challenges.

## Set denoising mode

<img />

* **No denoising**: disables all audio preprocessing and passes the raw audio signal directly to the ASR model. The ASR model itself can handle a minimal level of ambient noise without preprocessing. Choose this mode if you experience issues with missing short responses (e.g. "sure", "yes") or degraded accuracy with non-English transcription, particularly when background noise is not significant.
* **Remove noise** (default): removes background noise with nearly no distortion to the waveform, so it has no meaningful impact on speech-to-text accuracy. It will not remove loud background speech.
* **Remove noise + background speech**: a more aggressive mode that removes both background noise and background speech. This may distort the waveform and can reduce speech-to-text accuracy in some cases. This option incurs a \$0.005/min surcharge due to the additional processing required.

If your use case typically involves loud background speech — such as a TV or a construction site — try the `Remove noise + background speech` mode. For most use cases, `Remove noise` is the recommended default. If the environment is quiet and transcription completeness is the priority, use `No denoising`.

## Tuning interruption sensitivity

The denoising mode setting is to combat background speech and noise before the transcription is generated. And even with those in place, there can still be cases of unwanted interruptions. You can configure the interruption sensitivity to reduce these cases. Set it lower if you want agent to be more resilient to background speech or user interruptions.

1. In the same settings panel
2. Set the "Interruption Sensitivity" to 0.8
3. This setting helps the agent reduce false interruptions from background speech and noise

<Frame>
  <img />
</Frame>

For extremely noisy environments, you may need to experiment with even higher settings. Note that this setting will hinder the ability of your agent getting interrupted, so it's a trade off you need to make.

## Remove noise from the user's side

As the audio quality is determined by the user's side, you can also try the following:

* User side noise reduction: use better microphone & client side noise reduction libraries if using web calls
* Prompt the agent to ask your users to speak louder so it can be distinguished from background speech easier


# Handle voicemail and IVR
Source: https://docs.retellai.com/build/handle-voicemail

Configure your AI agent to detect and handle voicemails and IVR systems automatically

When making outbound calls, your phone agent may encounter voicemails or IVR (Interactive Voice Response) systems. You can configure your agent to automatically detect these and take appropriate action.

<Frame>
  <img />
</Frame>

## Voicemail detection

The system runs voicemail detection continuously within a timeout window. You can choose what happens when a voicemail is detected:

* **Hang up** — disconnect immediately, even if the voicemail greeting is still playing.
* **Leave a message** — wait for the agent's turn to speak, then deliver a message. Supports [dynamic variables](/build/dynamic-variables).

If the timeout is reached without detecting a voicemail, detection stops and the call continues normally.

<Steps>
  <Step title="Enable voicemail detection">
    Navigate to your agent settings, then open **Call Settings** and enable **Voicemail Detection**.
  </Step>

  <Step title="Choose voicemail behavior">
    Select one of the following options:

    * **Hang up if reaching voicemail**: The agent disconnects when it detects a voicemail.
    * **Leave a message if reaching voicemail**: The agent waits for its turn to speak, then leaves a message. Choose between:
      * **Prompt**: A dynamically generated message based on instructions you provide, such as `Summarize the call and ask the user to call back.`
      * **Static Sentence**: A fixed message, such as `Hey {{user_name}}, sorry we could not reach you directly. Please give us a callback if you can.`
  </Step>
</Steps>

## IVR hangup

When enabled, the system detects if your outbound call reaches an IVR (automated phone menu) system and automatically hangs up the call.

<Note>
  IVR hangup is separate from [IVR navigation](/build/telephony/navigate-ivr), which allows your agent to interact with and navigate through IVR menus using DTMF tones.
</Note>

To enable, navigate to your agent settings, then open **Call Settings** and toggle on **IVR Hangup**.

## FAQ

<AccordionGroup>
  <Accordion title="The voicemail isn't being hung up even though hang up is enabled. What's wrong?">
    This most likely means the call is being classified as an IVR rather than a voicemail. Because the two detection types are handled separately, voicemail hang up will not trigger in this case. Enable **IVR Hangup** in your agent's **Call Settings** to handle this scenario and automatically disconnect when an IVR system is detected.
  </Accordion>

  <Accordion title="Will voicemail or IVR detection run for the entire call?">
    No, voicemail and IVR detection will only run for the first 3 minutes of the call. Please contact [support@retellai.com](mailto:support@retellai.com) if you need to extend this.
  </Accordion>

  <Accordion title="Is there a latency impact when using voicemail detection?">
    Voicemail detection is optimized for real-time use cases and generally adds under 30ms of latency.
  </Accordion>

  <Accordion title="How can I tell if a call reached a voicemail or IVR?">
    If voicemail is detected, the call will have a disconnection reason of `voicemail_reached`. If IVR is detected, the disconnection reason will be `ivr_reached`.
  </Accordion>

  <Accordion title="If the voicemail greeting keeps playing, will the agent hang up?">
    Yes. When set to hang up, the agent disconnects immediately upon detection, regardless of whether the voicemail greeting is still playing.
  </Accordion>

  <Accordion title="If the voicemail greeting keeps playing, will the agent leave a message?">
    No. When set to leave a message, the agent waits for its turn to speak before delivering the message.
  </Accordion>
</AccordionGroup>


# Add backchannel
Source: https://docs.retellai.com/build/interaction-configuration

Enable and customize backchanneling in Retell AI to enhance call engagement with natural responses.

<Frame>
  <img alt="Backchannel configuration settings showing frequency and word options" />
</Frame>

Backchannel is the ability for the agent to make small noises like "uh-huh", "I see", etc. during user speech, to
improve engagement of the call. You can set whether to enable it, how often it triggers, what words are used.

You will look at the following fields in [Create Agent API](/api-references/create-agent):

* `enable_backchannel`: set to `true` to enable backchannel. Default to `false`.
* `backchannel_frequency`: When our engine determines that a backchannel is possible and appropriate here, you don't necessarily always want
  to backchannel. Humans often only backchannel at some places, not all possible cases. Therefore, this field controls how often
  the backchannel is triggered, with 0 being never, 1 being always when possible. The default is 0.8.
* `backchannel_words`: The words that the agent can use as backchannel. The default is different for each language, and for each
  voice provider, as some voice provider does not have support for some of the words. The following tab contains the default backchannel
  words for each language and voice provider. You can overwrite this field to customize the backchannel words.
  Note that certain voices do not work too well with certain words, so it's recommended to experiment before adding any words.

  <Tabs>
    <Tab title="en">
      * `11labs voices`: \["okay", "uh-huh", "mhmm", "yah"]
      * `openai voices`: \["okay", "uh-huh", "yah"]
      * `deepgram voices`: \["okay", "uh-huh", "yah"]
    </Tab>

    <Tab title="es">
      * `11labs voices`: \["mhm", "ajá", "si", "vale"]
      * `openai voices`: \["ajá", "si", "vale"]
    </Tab>

    <Tab title="hi">
      * `11labs voices`: \["अरे", "हाँ", "उम्म", "अच्छा", "सही", "ओह"]
      * `openai voices`: \["अच्छा", "सही"]
    </Tab>

    <Tab title="de">
      * `11labs voices`: \["mhm", "ja", "genaú"]
      * `openai voices`: \["ja"]
    </Tab>

    <Tab title="fr">
      * `11labs voices`: \["mhm", "oui"]
      * `openai voices`: \["oui"]
    </Tab>

    <Tab title="ja">
      * `11labs voices`: \["はい"]
      * `openai voices`: \["はい"]
    </Tab>

    <Tab title="pt">
      * `11labs voices`: \["certo", "sim", "tá"]
      * `openai voices`: \["sim"]
    </Tab>
  </Tabs>


# Knowledge Base
Source: https://docs.retellai.com/build/knowledge-base

Enhance AI agent with a knowledge base using URLs, documents, and custom text for better responses.

## Overview

Knowledge base are a collection of sources of information that your agent can access to retrieve relevant information during the call, that can provide additional context to the conversation. It can greatly improve the quality of the responses and the overall experience, especially in cases where there are a lot of information available (too long for putting in prompt), but having the information is essential for the agent to respond correctly. This feature quite useful for use cases like support, helpdesk, FAQ, etc.

Supported sources:

* Website content (via URLs)
* Documents (supported formats: .bmp, .csv, .doc, .docx, .eml, .epub, .heic, .html, .jpeg, .png, .md, .msg, .odt, .org, .p7s, .pdf, .png, .ppt, .pptx, .rst, .rtf, .tiff, .txt, .tsv, .xls, .xlsx, .xml)
* Custom text snippets

### How it works

You can create knowledge bases, and link them to your agents. When a knowledge base is linked to an agent, the agent will always try to retrieve information from the knowledge base before responding. There's no need to change your prompt for it to trigger, as it will be done automatically, for every response generation.

During the creation of knowledge bases, it will chunk the source, embed them and store into a vector database.

During the call, when the agent is about to respond, it will use the transcript so far (prompt is not included) to find the most relevant chunks from the knowledge base, and feed them to the LLM as context.

### Auto-refreshing and auto-crawling

You can enable auto-refreshing and/or auto-crawling for URL sources in your knowledge base.

* Auto-refreshing: When enabled, the system re-fetches all URLs in the knowledge base every 24 hours to ensure the latest content is reflected.

* Auto-crawling: You can enable this feature for specific URL paths. The system will automatically crawl all pages under each path every 24 hours, excluding any URLs you’ve added to the exclusion list. All pages found—except those explicitly excluded—will be stored.

### Limits

Each knowledge base has the following limits:

* URL: at max 500 urls.
* Auto-Crawling URL Paths: at max 200 exclusion urls for each auto-crawling path, and at max 500 exclusion URLs per knowledge base.
* Text: at max 50 text snippets
* File: at max 25 files, with each file at max 50MB. For CSV, TSV, XLS, and XLSX, the row limit is 1000 rows and the column limit is 50 columns.

You can create multiple knowledge bases to overcome these limits. An agent can have more than one knowledge bases linked to it.

## Best Practices

* Prefer `.md` (Markdown) files over `.txt`. Well-structured Markdown is chunked and retrieved more accurately.
  * Use clear, descriptive headings and keep each `##` section focused and reasonably short. If a `##` becomes long, split it into multiple `##`/`###` sections.
  * Write short paragraphs and lists to separate concepts; avoid walls of text.
  * For tabular or image-heavy content, retrieval may be less reliable; consider adding explanatory text so related information stays in the same chunk.
* Group related information within the same section so chunks remain cohesive and relevant.
* Avoid ambiguity and use specificity in references. Include names, dates, units, and avoid ambiguous pronouns like `it` or `this`, because prior chunks may not be present.
* Use more granular paths for auto-crawling instead of broad paths with many exclusion URLs. This improves crawl performance and helps avoid hitting the exclusion URL limits.
* Use the knowledge base to supply supporting information, not agent instructions or prompts. Put instructions in the agent's prompt.

## Use Knowledge Base

<Steps>
  <Step title="Access Knowledge Base Settings">
    1. Navigate to your dashboard
    2. Select the "Knowledge Base" tab
    3. Click the "Add" button in the top-right corner

    <Frame>
      <img alt="Knowledge Base dashboard view" />
    </Frame>
  </Step>

  <Step title="Create Knowledge Base Items">
    Choose from three types of knowledge sources:

    1. **URL**: Import content from web pages
       * Supports single pages or entire websites
       * Automatically updates when content changes

    2. **File**: Upload documents
       * Supported formats: PDF, TXT, DOCX, etc.
       * Maximum file size: 50MB

    3. **Text**: Add custom content
       * Paste or type direct information
       * Ideal for specific instructions or data

    <Frame>
      <img alt="Adding knowledge base items" />
    </Frame>
  </Step>

  <Step title="Enable auto-crawling">
    Auto-crawling can be enabled for individual URL paths. URLs that are not selected will be added to the exclusion list and excluded from the knowledge base.

    You can edit auto-crawling paths to add or remove URLs from the exclusion list. Previously crawled URLs (displayed in bold) can be excluded, and URLs currently on the exclusion list can be reinstated.

    <Frame>
      <img alt="Adding an auto-crawling path" />
    </Frame>

    <Frame>
      <img alt="Editing an auto-crawling path" />
    </Frame>

    <Frame>
      <img alt="Editing the exclusion list" />
    </Frame>
  </Step>

  <Step title="Verify Added Items">
    After adding items, they will appear in your knowledge base list. You can:

    * View all added items
    * Edit existing items
    * Delete items when no longer needed

    <Frame>
      <img alt="Knowledge base items list" />
    </Frame>
  </Step>

  <Step title="Connect to Your Agent">
    1. Open the agent editor
    2. Locate the "Knowledge Base" section
    3. Select the knowledge base items you want to use

    <Frame>
      <img alt="Connecting knowledge base to agent" />
    </Frame>
  </Step>

  <Step title="Configure Knowledge Base Settings">
    After connecting a knowledge base to your agent, you can configure how many chunks are retrieved via "Adjust KB Retrieval Chunks and Similarity".

    * Chunks to retrieve: The max number of chunks to retrieve from the knowledge base, range 1-10. Default: 3.
    * Similarity Threshold: Adjust how strict the system is when matching chunks to the context. A higher setting gives you fewer, but more similar, matches. Default: 0.6.

    Note: Increasing "Chunks to retrieve" gives the LLM more context, but also increases the prompt length and can interfere with generation quality. For most cases, the recommended settings are 3 chunks and a 0.60 similarity threshold.

    <Frame>
      <img alt="Adjust knowledge base retrieval chunks and similarity settings" />
    </Frame>
  </Step>

  <Step title="Setup Node Level Knowledge Base">
    For Conversation Flow Agent, you can configure knowledge base at both Conversation Node level and Subagent Node level. Node-level knowledge base will be combined with the agent-level knowledge base to provide more accurate context for a specific topic.

    1. Open the agent editor
    2. Click the Conversation Node or Subagent Node you want to configure.
    3. Similar to agent level knowledge base config above, you can select and add the knowledge base items you want to use.

    <Frame>
      <img alt="Config node level knowledge base" />
    </Frame>
  </Step>
</Steps>

Your agent will now use this information when responding to queries related to the added content. Retrieved knowledge base content will be appended to the LLM prompt under the header **## Related Knowledge Base Contexts**.

## FAQ

<AccordionGroup>
  <Accordion title="Do I need to change my prompt to use knowledge base?">
    No, you don't need to change your prompt. It will be used automatically when added to an agent.
  </Accordion>

  <Accordion title="How can I prevent the LLM from generating information not found in the knowledge base?">
    You can add the following prompt to the agent:

    ```
    Only answer using the information in ## Related Knowledge Base Contexts.
    If ## Related Knowledge Base Contexts is missing or does not contain relevant information, respond:
    "There is no related information in knowledge base."
    ```
  </Accordion>

  <Accordion title="The agent response is not correct, what should I do?">
    Please check the knowledge base documents to see if the information is correct. And check the format of the source as suggested above, markdown format with clear paragraphs is recommended.
  </Accordion>

  <Accordion title="Will this add a long latency to the call?">
    We've optimized Knowledge Base retrival latency for real time use case, so it should generally be under 100ms of latency impact.
  </Accordion>

  <Accordion title="Is there a way to check what's getting retrieved from the knowledge base?">
    We're working on adding this feature to expose this information soon.
  </Accordion>

  <Accordion title="Will the knowledge base name influence the retrieval?">
    No, the name is for display purpose only. It's not included in the retrieval process.
  </Accordion>
</AccordionGroup>

## Pricing

* Knowledge base creation:
  * First 10 knowledge bases are free.
  * Additional ones are billed at \$8 / month per knowledge base.
* Using knowledge base:
  * \$0.005 per minute of calls that have knowledge base enabled.
  * it does not matter if your agent is using 1 or many knowledge bases, the billing is the same.


# Configure LLM Options
Source: https://docs.retellai.com/build/llm-options

Optimize your agent's language model settings for reliability, performance, and cost

## Overview

LLM (Large Language Model) configuration options allow you to fine-tune how your agent processes and responds to conversations. Different settings can dramatically impact your agent's behavior, reliability, and cost.

<Note>
  Not all options are available for every model. Check your dashboard for model-specific capabilities.
</Note>

<Frame>
  <img alt="LLM configuration panel showing temperature, structured output, and fast tier options" />
</Frame>

## Temperature Settings

### What is Temperature?

Temperature controls the randomness and creativity of your agent's responses. It's a value typically between 0 and 1 that affects how the model selects its next words.

### Temperature Guidelines

| Temperature   | Behavior                           | Best For                                             |
| ------------- | ---------------------------------- | ---------------------------------------------------- |
| **0.0 - 0.3** | Highly consistent, deterministic   | Function calling, data collection, technical support |
| **0.4 - 0.7** | Balanced consistency and variation | General customer service, sales calls                |
| **0.8 - 1.0** | Creative, varied responses         | Creative brainstorming, casual conversation          |

### Recommendations by Use Case

* **Appointment Booking**: Use 0.1-0.3 for accurate data capture
* **Customer Support**: Use 0.3-0.5 for consistent yet natural responses
* **Sales Outreach**: Use 0.5-0.7 for engaging but focused conversations
* **Virtual Companion**: Use 0.7-0.9 for more human-like variation

## Structured Output

### Purpose

Structured Output ensures that LLM responses strictly follow predefined schemas, particularly important for reliable function calling. When enabled, the model is constrained to output only valid function calls with all required parameters.

### Benefits

* **Increased Reliability**: Eliminates missing or malformed function arguments
* **Better Error Handling**: Prevents invalid function calls from being attempted
* **Consistent Data Format**: Ensures all outputs match expected schemas

### Trade-offs

* **Slower Auto-save**: Schema caching may delay agent configuration saves
* **Less Flexibility**: Model cannot deviate from defined structures
* **Initial Setup Time**: First load after changes may be slower

### When to Use

✅ **Enable for:**

* Production agents with critical function calls
* Agents handling financial or medical data
* Integration with strict API requirements

❌ **Consider disabling for:**

* Development and testing phases
* Agents with simple or flexible function needs
* When rapid iteration is more important than reliability

## Fast Tier (Premium Performance)

### What is Fast Tier?

Fast Tier routes your LLM calls through dedicated, high-priority infrastructure for superior performance and consistency. This premium option eliminates the variability you might experience with standard routing.

### Key Benefits

1. **Consistent Latency**: Predictable response times for every call
2. **Higher Availability**: Priority access to compute resources
3. **Reduced Variance**: Minimal fluctuation in processing speeds
4. **Better User Experience**: Smoother, more natural conversations

### Cost Consideration

<Warning>
  Fast Tier pricing is **1.5x the standard rate** for your selected model. Calculate the ROI based on your use case before enabling.
</Warning>

### When to Use Fast Tier

✅ **Ideal for:**

* High-value customer interactions
* Time-sensitive operations (emergency services, urgent support)
* Premium service tiers
* Demonstrations and sales calls

❌ **May not be necessary for:**

* Internal testing
* Low-volume or non-critical calls
* Cost-sensitive applications

<Frame>
  <img alt="Performance comparison chart showing improved latency consistency with Fast Tier enabled" />
</Frame>

### Performance Impact

Based on our benchmarks:

* **50% reduction** in latency variance
* **25% improvement** in average response time
* **99.9% availability** vs 99.5% standard


# Make agent hold and respond nothing
Source: https://docs.retellai.com/build/no-response



Sometimes you might want the agent to hold and not respond to the user, like when user says "hold on" or "give me a minute".

We hard-coded a stop sequence in the LLM: `NO_RESPONSE_NEEDED`. Whenever this sequence is met, the response generation stops.
You can then prompt the LLM to output nothing by writing something like:

```
- if user says "hold on", reply exactly the following: "NO_RESPONSE_NEEDED".
```


# Platform voices
Source: https://docs.retellai.com/build/platform-voices

Retell's curated voice library, optimized for real-time phone conversations.

Platform voices are Retell's curated voice library, fine-tuned specifically for conversational AI over the phone. They handle fillers, pacing, and conversational rhythm well, and are calibrated for clarity at telecom bitrates.

When using a platform voice, fallback is handled automatically to maintain the same voice experience — you do not need to configure a TTS fallback plan in Security & Fallback Settings.

<Note>
  If you are using a non-platform voice, you will need to [configure TTS fallback](/build/tts-fallback) manually.
</Note>

## Select a platform voice

Platform voices are available in the voice selector in your agent settings. You can preview each voice directly in the dashboard before selecting.

## Custom voice cloning

You can clone your own voice as a platform voice by setting `voice_provider` to `platform` when calling the [Clone Voice](/api-references/clone-voice) API. The cloned voice will behave the same as a built-in platform voice — fallback is handled automatically and you do not need to configure TTS fallback separately.


# Prompt Engineering Guide
Source: https://docs.retellai.com/build/prompt-engineering-guide

Best practices for writing effective prompts that create reliable and natural-sounding AI phone agents

## Introduction

Prompt engineering is the foundation of creating effective AI phone agents. A well-crafted prompt determines how your agent interprets situations, responds to users, and handles edge cases. This guide provides proven strategies for writing prompts that agents can follow reliably.

<Note>
  This guide focuses on general prompt engineering principles. For agent-specific implementation:

  * **Single/Multi Prompt Agents**: Apply these principles directly in your prompts
  * **Conversation Flow Agents**: Use these principles within individual node instructions
</Note>

## Getting Started

To see examples of effective prompts, create a new agent in the Dashboard and explore our pre-built templates. These templates demonstrate best practices for various use cases.

## Best Practice 1: Use Sectional Prompts

Break large prompts into focused sections for better organization and LLM comprehension. This structured approach offers several benefits:

* **Reusability**: Sections can be adapted across different agents
* **Maintainability**: Easy to update specific behaviors without affecting others
* **Clarity**: LLMs process structured information more accurately

### Recommended Prompt Structure

```markdown theme={null}
## Identity
You are a friendly AI assistant for [Company Name].
Your role is to [specific purpose].
You have expertise in [relevant domains].

## Style Guardrails
Be concise: Keep responses under 2 sentences unless explaining complex topics.
Be conversational: Use natural language, contractions, and acknowledge what the caller says.
Be empathetic: Show understanding for the caller's situation.

## Response Guidelines
Return dates in spoken form: Say "January fifteenth" not "1/15".
Ask one question at a time: Avoid overwhelming the caller with multiple questions.
Confirm understanding: Paraphrase important information back to the caller.

## Task Instructions
[Specific steps the agent should follow]

## Objection Handling
If the caller says they're not interested: "I understand. Is there anything specific..."
If the caller is frustrated: "I hear your frustration, let me help resolve this..."
```

## Best Practice 2: Use Conversation Flow for Complex Tasks

When your agent needs to handle complex logic or multiple tools, consider using Conversation Flow agents instead of trying to manage everything in a single prompt.

### When to Switch to Conversation Flow:

* **Multiple decision branches**: More than 3-4 conditional paths
* **Tool coordination**: Using 5+ different functions/tools
* **State management**: Tracking multiple variables throughout the conversation
* **Reliability concerns**: Single prompt shows inconsistent behavior

### Benefits of Conversation Flow:

* Each node focuses on one specific task
* Deterministic tool calling and transitions
* Easier to debug and optimize individual steps
* More predictable agent behavior

## Best Practice 3: Explicit Tool Calling Instructions

<Note>This section applies only to Single/Multi Prompt Agents. Conversation Flow Agents handle function calls deterministically through their node configuration.</Note>

### The Challenge

LLMs often struggle to determine when to call tools based solely on tool descriptions. Without explicit instructions, agents may:

* Call tools at inappropriate times
* Fail to call tools when needed
* Use the wrong tool for a situation

### Solution: Define Clear Triggers

Always specify exact conditions for tool usage in your prompts. Reference tools by their exact names.

#### Example: Customer Service Agent

```markdown theme={null}
## Tool Usage Instructions

1. Gather initial information about the customer's issue.

2. Determine the type of request:
   - If customer mentions "refund" or "money back":
     → Call function `transfer_to_support` immediately
   - If customer needs order status:
     → Call function `check_order_status` with order_id
   - If customer wants to change their order:
     → First call `check_order_status`
     → Then transition to modification_state

3. After retrieving information:
   - Always summarize what you found
   - Ask if they need additional help
   - If yes, determine next appropriate action
```

### Best Practices for Tool Instructions

1. **Use trigger words**: List specific words/phrases that should trigger tool calls
2. **Define sequences**: Specify when tools should be called in order
3. **Set boundaries**: Clarify when NOT to call certain tools
4. **Provide context**: Explain why each tool is being called


# Prompt guide & examples for specific situations
Source: https://docs.retellai.com/build/prompt-situation-guide



Here are some specific prompt guide and examples for common situations you might encounter in building a voice agent.

<Tip>Many of these patterns — including phone number pronunciation, email spelling, and speech normalization — are now available as one-click presets in the [Agent Handbook](/build/agent-handbook).</Tip>

## Pronounce the phone numbers

We'll utilize the Read Slowly feature to add pauses between words. For more information, see the [Speech Controllability documentation](https://docs.retellai.com/agent/speech-controllability#add-pauses-how-to-read-slowly).

It's recommended to include a prompt as a guideline for the LLM to follow. This ensures that the agent can consistently reply with the correct format, even if customers double-check the phone number.

```
When people ask about your phone number, your phone number is 4158923245

## Guideline
When speaking the phone number, transform the format as follows:
- Input formats like 4158923245, (415) 892-3245, or 415-892-3245
- Should be pronounced as: "four one five - eight nine two - three two four five"
- Important: Don't omit the space around the dash when speaking
```

Listen to this audio clip for a demonstration of proper phone number pronunciation:

[Speak Phone Number Example](https://retell-utils-public.s3.us-west-2.amazonaws.com/speak_phone_number.wav)

## Pronounce the email

```
## How to spell out
The possible email format is name@company.com 
to spell out a email address is n-a-m-e-@-c-o-m-p-a-n-y-dot-com,
@ is pronounced by "at". 
```

## Pronounce the website

```
Whenever you encounter a website URL, please:
Identify each segment of the domain name.
If a segment consists of individual letters (e.g., "NK"), pronounce each letter using its spoken form in English (e.g., "N" → "en," "K" → "kay").
If a segment is a recognizable word (e.g., "laundry"), pronounce it normally as that word.
Pronounce "dot" before stating the top-level domain (e.g., "dot com," "dot net," "dot org," etc.).
Example:
"nklaundry.com" → "en-kay-laundry dot com"
"abctest.net" → "A B C test dot net"
"xyzco.org" → "ex-why-zee-co dot org"
Adhere to this phonetic breakdown carefully to ensure clarity and proper pronunciation for customers.
```

## Pronounce the time

```
For State Numbers, Times & Dates
For 1:00 PM, say "One PM."
For 3:30 PM, say "Three thirty PM."
For 8:45 AM, say "Eight forty-five AM."
Never say O'clock, Instead just say O-Clock.
Always say "AM" or "PM".
```

## Handle being put on hold / no response needed

### For non-reasoning models

We hard-coded a stop sequence in the LLM: `NO_RESPONSE_NEEDED`. Whenever this sequence is met, the response generation stops.
You can then prompt the LLM to output nothing by writing something like:

```
- when user says hold on, reply exactly the following: "NO_RESPONSE_NEEDED".
```

### For reasoning models

<Warning>
  Reasoning models like `gpt 5`, `gpt-5.1` does not support this feature. You need to prompt engineer it differently to achieve this.
</Warning>

You can try the following prompt: `When user says hold on, simply do not respond`.


# Code Tool
Source: https://docs.retellai.com/build/single-multi-prompt/code-tool

Run JavaScript code directly in your agent without an external server

Code Tool lets your agent execute JavaScript code as a function call — no external server needed. Unlike [custom functions](/build/single-multi-prompt/custom-function) that send HTTP requests to your endpoint, code tools run directly in Retell's sandbox.

The LLM decides when to call the code tool based on the function name, description, and conversation context.

<Warning>
  Code Tool is designed for lightweight logic like formatting, calculations, and simple read-only lookups. Do not use it to access internal systems, write to production databases, or handle sensitive credentials. Both `dv` and `metadata` values are stored in plaintext with every call record. For integrations that require authentication, secrets management, or write access, use a [Custom Function](/build/single-multi-prompt/custom-function) hosted on your own backend. See [Security and Architecture Guidance](#security-and-architecture-guidance) for details.
</Warning>

## Create a Code Tool

<Steps>
  <Step title="Add a Code Tool">
    In the agent's **Functions** section, click **+ Add** and select **Code**.

    <Frame>
      <img alt="Function type dropdown showing the Code option" />
    </Frame>
  </Step>

  <Step title="Set name and description">
    * **Name**: A unique identifier (alphanumeric, dashes, underscores). Example: `calculate_shipping_cost`
    * **Description**: Explain what the tool does and when to call it. The LLM uses this to decide when the function is appropriate. Example: "Calculate shipping cost based on the customer's zip code and order weight."
  </Step>

  <Step title="Write JavaScript">
    Write your JavaScript code in the editor. You have access to dynamic variables, call metadata, and the `fetch` function for HTTP requests. See [JavaScript Environment](#javascript-environment) below for details.

    <Frame>
      <img alt="Code Tool editor with name, description, code, and configuration options" />
    </Frame>

    ```javascript theme={null}
    // Example: calculate shipping based on dynamic variables
    const weight = parseFloat(dv.order_weight);
    const zone = dv.shipping_zone;

    let cost;
    if (zone === "local") {
      cost = weight * 0.5;
    } else if (zone === "domestic") {
      cost = weight * 1.2;
    } else {
      cost = weight * 3.0;
    }
    return { shipping_cost: "$" + cost.toFixed(2), zone: zone };
    ```
  </Step>

  <Step title="Set response variables (optional)">
    Use **Store Fields as Variables** to extract values from your code's return value and save them as dynamic variables. Specify a variable name and the JSON path to the value.

    For example, if your code returns `{ "shipping_cost": "$6.00", "zone": "domestic" }`:

    | Variable Name   | JSON Path       | Extracted Value |
    | --------------- | --------------- | --------------- |
    | `shipping_cost` | `shipping_cost` | `"$6.00"`       |
    | `shipping_zone` | `zone`          | `"domestic"`    |
  </Step>

  <Step title="Configure speech settings">
    * **Speak During Execution**: When enabled, the agent says something while the code runs (e.g., "Let me calculate that for you."). Choose **Prompt** or **Static Text**.
    * **Speak After Execution**: When enabled (default), the LLM speaks about the result. Turn off if you want the tool to run silently.
  </Step>

  <Step title="Update your prompt">
    Guide the LLM on when to use the code tool in your agent's prompt. For example:

    ```
    When the customer asks about shipping costs, use the calculate_shipping_cost
    tool to compute the cost based on their order details.
    ```
  </Step>

  <Step title="Test your code">
    Click **Run Code** at the bottom of the editor to test. Use the **Dynamic Variables** dropdown in the editor to set test values for your variables (e.g., give `order_weight` a value of "5") — these values are only used during testing and won't affect your live agent. The output panel will show the result and any `console.log()` output.

    <Frame>
      <img alt="Code Tool editor showing test output after clicking Run Code" />
    </Frame>
  </Step>
</Steps>

## JavaScript Environment

Your code runs in a JavaScript sandbox with the following globals available. The code editor provides **autocomplete** — as you type, it will suggest available globals, dynamic variable names, and built-in functions.

### `dv` — Dynamic Variables

Access your agent's dynamic variables as properties on the `dv` object. All values are strings.

```javascript theme={null}
const name = dv.customer_name;       // "John Doe"
const orderId = dv.order_id;         // "78542"
const total = parseFloat(dv.amount); // Convert to number if needed
```

### `metadata` — Call Metadata

Access metadata passed when the call was created via the API. This is the same object you pass in the `metadata` field of the [Create Call](/api-references/create-phone-call) API.

```javascript theme={null}
const customerId = metadata.customer_id;
const priority = metadata.priority_level;
```

<Warning>
  Both `dv` and `metadata` values are stored in plaintext with every call record and are visible in call logs and API responses. Do not use them to pass API keys, database credentials, or other sensitive secrets. See [Security and Architecture Guidance](#security-and-architecture-guidance) for more details.
</Warning>

### `fetch(url)` — HTTP Requests

Make HTTP requests to external APIs. Works like the standard [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API).

```javascript theme={null}
// GET request
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// POST request
const response = await fetch("https://api.example.com/submit", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: dv.customer_name })
});
```

### `console.log()` — Debugging

Log output for debugging. Logs appear in the test output panel when using **Run Code**.

```javascript theme={null}
console.log("Customer:", dv.customer_name);
console.log("API response:", JSON.stringify(data));
```

<Note>
  * Your code can return any value (object, string, number) or return nothing at all.
  * Standard JavaScript built-ins are available: `Math`, `JSON`, `Date`, `Array`, `Object`, `String` methods, etc.
  * External packages (`require`, `import`) are **not** available. Use `fetch()` for external integrations.
  * Code is limited to 5,000 characters.
</Note>

## Examples

### Format data from dynamic variables

```javascript theme={null}
// Combine and format customer info
const fullName = dv.first_name + " " + dv.last_name;
const summary = `Customer ${fullName} (ID: ${dv.customer_id}) requested a callback.`;
return { full_name: fullName, summary: summary };
```

### Fetch data from a public API

```javascript theme={null}
// Look up current weather for the customer's city
const response = await fetch("https://api.weatherapi.com/v1/current.json?q=" + encodeURIComponent(dv.city));
const weather = await response.json();
return {
  location: weather.location.name,
  temperature: weather.current.temp_f + "°F",
  condition: weather.current.condition.text
};
```

### Conditional logic with API call

```javascript theme={null}
// Route based on customer tier
const response = await fetch("https://api.example.com/customers/" + dv.customer_id);
const customer = await response.json();

if (customer.tier === "premium") {
  return { action: "priority_support", wait_time: "0 minutes" };
} else if (customer.tier === "standard") {
  return { action: "standard_queue", wait_time: "5 minutes" };
} else {
  return { action: "general_queue", wait_time: "10 minutes" };
}
```

## Security and Architecture Guidance

Code Tool is best for lightweight, low-risk logic that runs entirely within Retell's sandbox. As your integration needs grow, use a [Custom Function](/build/single-multi-prompt/custom-function) hosted on your own backend where you control the security boundary.

| Use case                                                                             | Recommended             |
| ------------------------------------------------------------------------------------ | ----------------------- |
| Formatting, calculations, string cleanup                                             | Code Tool               |
| Simple read-only lookups to low-risk public APIs                                     | Code Tool, with caution |
| Accessing internal systems or private APIs                                           | Custom Function         |
| Writing to CRM, EHR, booking, payment, or ticketing systems                          | Custom Function         |
| Workflows requiring secrets, audit logs, retries, idempotency, or policy enforcement | Custom Function         |

<Warning>
  **Do not treat dynamic variables or metadata as a secret vault.** Avoid placing long-lived API keys, database credentials, or other sensitive secrets in dynamic variables or call metadata for use in Code Tool. Both `dv` and `metadata` values are stored in plaintext with every call record — anything you pass in will be visible in call logs and API responses. They are not designed for secret management. Prefer short-lived tokens where possible, and use a [Custom Function](/build/single-multi-prompt/custom-function) for integrations that require sensitive credentials or customer-controlled secret handling.
</Warning>

<Warning>
  **Use `fetch()` with caution.** Enabling outbound HTTP requests from an LLM-invoked tool increases security and operational risk. Treat any use of `fetch()` as an external integration surface. Prefer read-only requests to low-risk, public endpoints. Avoid direct state-changing actions (writes, payments, deletions) unless you fully understand the risks and have appropriate controls in place.
</Warning>

<Note>
  **Keep production logic in your own backend.** For anything involving sensitive credentials, direct writes to production systems, payment actions, regulated data workflows, or business-critical operations that require strict authentication, validation, audit logging, idempotency, or approval controls — use a [Custom Function](/build/single-multi-prompt/custom-function) hosted on your own backend. Code Tool should be reserved for data transformation, calculations, and simple read-only lookups.
</Note>

## Response Variables

Response variables let you extract specific values from your code's return value and store them as dynamic variables.

Specify each variable as a **name** and a **JSON path** using dot notation:

| Path Syntax     | Example         | Extracts               |
| --------------- | --------------- | ---------------------- |
| Top-level field | `status`        | `result.status`        |
| Nested field    | `data.order.id` | `result.data.order.id` |
| Array element   | `items[0].name` | First item's name      |

If a path doesn't exist in the return value, the variable is skipped (no error).

## Configuration

* **Timeout**: How long the code can run before timing out. Range: 5–60 seconds. Default: 30 seconds.
* **Speak During Execution**: When enabled, the agent says something while the code runs. Choose between **Prompt** (LLM generates the message) or **Static Text** (exact text you provide). Recommended when your code takes more than 1 second.
* **Speak After Execution**: When enabled (default), the LLM speaks about the result after execution. Turn off to run the tool silently (e.g., for background logging).

<Note>
  The code result is capped at 15,000 characters to prevent overloading the LLM context.
</Note>

## FAQ

<AccordionGroup>
  <Accordion title="Can I use npm packages or external libraries?">
    No. The code runs in a lightweight JavaScript sandbox without access to `require` or `import`. You can use all standard JavaScript built-ins (`Math`, `JSON`, `Date`, `Array` methods, etc.) and the `fetch()` function for external API calls.
  </Accordion>

  <Accordion title="What happens if my code times out or throws an error?">
    If your code exceeds the timeout or throws an error, the execution is marked as failed and the error message is returned to the LLM. Response variables will not be extracted.
  </Accordion>

  <Accordion title="Can I use async/await?">
    Yes. The `fetch()` function is async, so you can use `await` to wait for HTTP responses. Top-level `await` is supported.
  </Accordion>

  <Accordion title="When should I use Code Tool vs Custom Function?">
    Use **Code Tool** for lightweight, low-risk logic — data formatting, calculations, and simple read-only lookups to public APIs. Use **Custom Function** when you need access to internal systems, databases, sensitive credentials, or any workflow that requires authentication, audit logging, idempotency, or write access to production systems. See [Security and Architecture Guidance](#security-and-architecture-guidance) for a detailed breakdown.
  </Accordion>
</AccordionGroup>


# Step 2: Configure the basic settings
Source: https://docs.retellai.com/build/single-multi-prompt/configure-basic-settings

Configure your AI agent with language models, voice settings and advanced customization.

Follow these steps to configure the fundamental settings for your agent, optimizing it for your specific business requirements.

<Steps>
  <Step title="Select a Language Model">
    We recommend starting with GPT-4.1, which offers an optimal balance of:

    * Response quality
    * Latency
    * Cost-effectiveness

    <Frame>
      <img alt="GPT-4 Turbo model selection" />
    </Frame>
  </Step>

  <Step title="Configure Voice Settings">
    1. Open the voice selection dropdown menu:

    <Frame>
      <img alt="Voice selection dropdown" />
    </Frame>

    2. Listen to the available voice samples and note the voice ID of your preferred option:

    <Frame>
      <img alt="Voice preview and selection" />
    </Frame>

    **Custom Voices**: You can also add voices from the ElevenLabs community by clicking "Add custom voice". Learn more in our [voice configuration guide](/build/voice).

    **Voice Speed**: You can adjust the agent's speaking speed using the Voice Speed slider (ranging from 0.5x to 2.0x) in the voice settings popover. If you check "Dynamically adjust based on user input", the agent will automatically adapt its speaking speed to match the user's pace during the call. It does this by tracking the user's words per minute and gradually shifting its own speed to align, making the conversation feel more natural. When dynamic voice speed is enabled, the user can also explicitly ask the agent to speak faster or slower, and the agent will adjust on the fly.
  </Step>

  <Step title="Configure Conversation Initiation">
    Define how your agent starts conversations:

    * **User-First**: Agent waits for user input
    * **Agent-First**: Agent initiates the conversation
      * Set a fixed welcome message
      * Use prompts to guide the agent's opening message

    <Frame>
      <img alt="Conversation initiation settings" />
    </Frame>
  </Step>
</Steps>

### More Settings

You can further customize your agent by setting the following settings:

<Steps>
  <Step title="Write Global Prompt">
    Here's where you specify the agent's persona, identity, guardrails, etc. This set of text will be available in every node, and will influence all response generation.
  </Step>

  <Step title="Configure Knowledge Base">
    Here's where you can supply contexts to agent via documents, urls, texts. Read more at [Knowledge Base Guide](/build/knowledge-base).
  </Step>

  <Step title="Configure Speech Settings">
    Here's a lot of options that allow you to finetune how your agent interacts with user.

    * Background sound: select a background sound that plays throughout the whole call to mimic an environment like call center, making the conversation more humanlike and engaging.
    * Responsiveness: how responsive the agent is. Set it lower if you want the agent to wait longer before responding, which can be useful when talking to folks like the elderly. The lower the value, the more wait time is added before the agent responds. You can also check "Dynamically adjust based on user input" to let the agent automatically tune its response timing during the call. When enabled, the agent observes how quickly the user speaks and adjusts accordingly — slower speakers get more patient response timing, while faster speakers get quicker responses.
    * Interruption Sensitivity: how fast the agent gets interrupted by user interruptions. Set it lower if you want agent to be more resilient to background speech.
    * Backchanneling: Set up how often and what words the agent uses to acknowledge users.
    * Boosted Keywords: Provides some biases towards certain words, making it easier to get recognized. Common ones are brand names, people's names, etc.
    * Speech Normalization: convert entities like date, currency, numbers into plain words, which can help prevent issues where audio generated was not pronouncing those right.
    * Reminder frequency: how often the agent will remind the user when user is inactive.
    * Pronunciation: set up pronunciation guide for specific words.
  </Step>

  <Step title="Configure Call Settings">
    Here's a couple of settings that's more call operation related.

    * Voicemail related settings: set up voicemail detection and what to do when voicemail is detected. See more at [Handle Voicemail](/build/handle-voicemail).
    * End call on silence: set up if user is active for a certain amount of time, the call will be ended.
    * Call duration: set up maximum duration of the call.
    * Pause before speaking: For the beginning of the call, if agent speaks first, it will wait for the configured duration before speaking, useful to handle scenarios when user is still picking up the phone.
  </Step>

  <Step title="Configure Post Call Analysis">
    Probably set up later, read more at [Post Call Analysis Guide](/features/post-call-analysis-overview).
  </Step>

  <Step title="Configure Privacy & Webhook">
    Here's where you can set up whether to opt out sensitive data storage, and configure webhook settings for receiving call related events.
  </Step>
</Steps>

### Video Tutorial

<iframe title="YouTube video player" />

See community templates in [docs](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope)

## Next Steps

Once you've configured these basic settings, your agent is ready for basic interactions. To enhance its capabilities, proceed to [adding capabilities by using function calling](/build/single-multi-prompt/function-calling).


# Integrate any system with custom function
Source: https://docs.retellai.com/build/single-multi-prompt/custom-function

Extend Retell AI with custom functions, integrating external APIs for advanced capabilities.

Custom functions allow you to extend your agent's capabilities by integrating external APIs, providing additional knowledge, or implementing custom logic.

## Steps to create a custom function

You can create custom functions that will be called by the LLM when needed. When called, Retell sends a POST request to your specified URL with the function name and parameters.

<Steps>
  <Step title="Add custom function in dashboard">
    Click "+ Add" in the tools section and select "Custom Function" from the dropdown menu.

    <Frame>
      <img alt="Adding custom function" />
    </Frame>
  </Step>

  <Step title="Configure function details">
    Add a name and description for the custom function. The name should be unique and separated with underscore.

    <Frame>
      <img alt="Custom function name and description fields" />
    </Frame>

    For example:

    * Name: `get_user_details`
    * Description: `Get user details based on name and age`
  </Step>

  <Step title="Select HTTP Method">
    Choose the HTTP method that Retell will use to send the request to your endpoint. Available methods include:

    <ul>
      <li><strong>GET</strong></li>
      <li><strong>POST</strong></li>
      <li><strong>PATCH</strong></li>
      <li><strong>PUT</strong></li>
      <li><strong>DELETE</strong></li>
    </ul>
  </Step>

  <Step title="Add endpoint URL">
    Add the URL where Retell will send the request to execute your custom function. This has to be a valid URL.
  </Step>

  <Step title="Set request headers (optional)">
    You can define custom headers to include with the request Retell sends to your endpoint.
    Header values can be static or include dynamic variables.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set query parameters (optional)">
    You can define query parameters to include in the request URL that Retell appends to your endpoint.
    There is a switch to change between parameter description or const value. Both description and const value could be dynamic variables.
    Description will be resolved by LLM while const value will be applied directly to the function.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Define parameters">
    Define the parameters for the custom function using JSON schema format or JSON form. Only available for POST, PATCH and PUT requests. For guidance, refer to:

    * [OpenAI's Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
    * [Function Calling Tutorial](https://semaphoreci.com/blog/function-calling)

    **Payload: args only**

    When **Payload: args only** is enabled, the JSON body is only the function's arguments: those fields appear at the top level of the request, not nested under `args`. When it is off, the body follows **Request & response spec** below (`name`, `call`, and `args`).

    <Tip>
      Turn this on when your endpoint expects a flat JSON body that matches your parameter object exactly, with no outer wrapper.
    </Tip>

    Example parameter schema:

    ```json theme={null}
    {
      "type": "object",
      "required": [
        "order_id"
      ],
      "properties": {
        "name": {
          "type": "object",
          "description": "",
          "properties": {
            "first_name": {
              "type": "string",
              "description": "User first name"
            },
            "last_name": {
              "type": "string",
              "const": "{{last_name}}"
            }
          }
        },
        "order_id": {
          "type": "number",
          "const": 1234
        }
      }
    }
    ```

    Example JSON form:

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set response variables (optional)">
    Extract values from the API response and save them as <strong>dynamic variables</strong> for use later in the conversation.

    For example, you can extract a user’s name from the response and reference it later using <code>\{\{user\_name}}</code>.

    Example response body

    ```javascript theme={null}
    {
      "properties": {
        "user": {
          "name": "John Doe",
          "age": 26
        }
      }
    }
    ```

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure speech behavior">
    Set up how the agent should handle speech during and after function execution. These two options are controling agent's behavior when user is not talking during the function call period. If user interrupts or talks, the agent would respond normally regardless of these settings.
    Note: both **Speak During Execution** and **Speak After Execution** are `Prompt` based. LLM will generate the message based on the config and the conversation.

    * **Speak during execution**: Whether the agent would speak the moment the function is called. Note that currently agent would speak just for one time during the beginning of the function call.
      * Enable for user-facing actions (e.g., getting weather information)
      * Disable for background tasks (e.g., attaching notes to call)

    * **Speak after execution**: Whether the agent would keep talking / do other actions (maybe call another function) after the function call is completed. You can use this to let agent tell user the result of the function call, continue the conversation, execute another task, etc after the function call is completed, without the need to wait for user to say anything to trigger a response.
      * Probably should enable for almost all cases, except for ones that are like press a digit kind of task where you don't expect the agent to keep talking.
  </Step>

  <Step title="Update prompt for function">
    It's best to include in the prompt explicitly when is the best time to invoke the custom function. For example:

    ```
    When user provided the city name, please get the weather for that city by calling the `get_weather` function.
    ```
  </Step>
</Steps>

### Troubleshooting

If you failed to save the custom function, it is likely because the parameters are not valid.

One common mistake is not adding `"type": "object",` to the top level of the JSON schema. We recommend clicking one of the examples and update accordingly.

## Request & response spec

Retell will send the request to your endpoint with the following request spec.

**Request**

* header
  * `X-Retell-Signature`: encrypted request body using your secret key, used to verify the request is from Retell. Read more below.
  * Content-Type: application/json. This indicates the payload is in JSON format.
* body (in JSON format, for POST, PUT and PATCH request)
  * `name`: the name of the custom function.
  * `call`: the call object for you to get more context about the call, it also contains real time transcript up to the time the request is sent. Check out [Get Call API](/api-references/get-call) for more details about the call object.
  * `args`: the arguments for the custom function, as a JSON object.

<Note>
  If **Payload: args only** is enabled for a function, the body is only the argument object (no `name`, `call`, or `args` wrapper). Parse parameters from the top level of the JSON, and run signature verification on that same body string.
</Note>

The request will timeout in your specified timeout period, or 2 minutes if not specified. When request fails, it will be retried up to 2 times.

**Response**

Response should have a status code between 200-299 to indicate success of HTTP request.
Response to the request can be in various format:

* string
* buffer
* JSON object
* blob

All these formats will be converted to string before sending to LLM for further processing.

<Note>
  The function result is capped at 15000 characters to prevent overloading LLM context window.
</Note>

## Verifying Request is from Retell

To verify that the request is coming from Retell, you can check the `X-Retell-Signature` header.

The value is a encrypted request body using your secret key.
For `GET` and `DELETE` requests, the request body is empty. You can use empty string in the verify function.

```javascript theme={null}
import { Retell } from "retell-sdk";
import express from "express";

const app = express();
// Use raw body for signature verification, not JSON.stringify(req.body).
app.use(express.raw({ type: "application/json" }));

app.post("/check-weather", async (req, res) => {
  const rawBody = req.body.toString("utf-8");
  if (
    !Retell.verify(
      rawBody,
      process.env.RETELL_API_KEY,
      req.headers["x-retell-signature"],
    )
  ) {
    console.error("Invalid signature");
    return;
  }
  const content = JSON.parse(rawBody);
  if (content.args.city === "New York") {
    return res.json("25f and sunny");
  } else {
    return res.json("20f and cloudy");
  }
});
```

```Python theme={null}
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from retell import Retell

retell = Retell(api_key=os.environ["RETELL_API_KEY"])

@app.post("/check-weather")
async def check-weather(request: Request):
    try:
        raw_body = (await request.body()).decode("utf-8")
        valid_signature = retell.verify(
            raw_body,
            api_key=str(os.environ["RETELL_API_KEY"]),
            signature=str(request.headers.get("X-Retell-Signature")),
        )
        if not valid_signature:
            print("Received Unauthorized")
            return JSONResponse(status_code=401, content={"message": "Unauthorized"})
        post_data = json.loads(raw_body)
        args = post_data["args"]
        if args["city"] == "New York":
            return JSONResponse(status_code=200, content={"result": "25f and sunny"})
        else:
            return JSONResponse(status_code=200, content={"result": "20f and cloudy"})
    except Exception as err:
        print(f"Error in webhook: {err}")
        return JSONResponse(
            status_code=500, content={"message": "Internal Server Error"}
        )
```

<Note>You can also secure your server from public network by only allowlisting Retell IP addresses: `100.20.5.228`</Note>


# End call
Source: https://docs.retellai.com/build/single-multi-prompt/end-call

Configure the Retell AI agent to end calls automatically based on user-defined conditions.

By default, the agent won't end the call automatically. You'll need to configure when and how the call should be terminated using the end call tool.

<Steps>
  <Step title="Add End Call Tool">
    Click "+ Add" in the tools section and select "End Call" from the dropdown menu.

    <Frame>
      <img alt="Adding end call tool" />
    </Frame>
  </Step>

  <Step title="Configure Termination Conditions">
    Define specific conditions under which the call should be terminated. For example:

    * "If the user says 'thank you', 'goodbye', or 'bye', use the end\_call tool to terminate the conversation."

    <Frame>
      <img alt="Configuring end call conditions" />
    </Frame>
  </Step>

  <Step title="Update the Prompt">
    Enhance the agent's understanding by incorporating the end call conditions into the prompt. Include specific instructions such as:

    "If the user says 'thank you', 'goodbye', or 'bye', use the end\_call tool to terminate the conversation."

    <Frame>
      <img alt="Adding end call instructions to prompt" />
    </Frame>
  </Step>
</Steps>


# Extract Dynamic Variables
Source: https://docs.retellai.com/build/single-multi-prompt/extract-dv



This tool lets you extract values from a user’s response and save them as dynamic variables.

## Steps

<Steps>
  <Step title="Add a Extract Dynamic Variable Tool">
    This would give your agent the ability to extract variable. The description is optional here.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Add Variables">
    Click "+Add" at the bottom and fill in the following details:

    <Frame>
      <img />
    </Frame>

    * **Variable Name** – A short name to reference this variable.
    * **Description** – A brief explanation of what this value should be.
    * **Variable Type** – Choose from `Text`, `Number`, `Enum`, or `Boolean`.
    * **Enum Options** - Options to choose from. Only when type is enum

    #### Variable Types

    You can create variables of the following types:

    * **Text** - Any word or sentence. Examples: `"headache"`, `"John Smith"`
    * **Number** - A numeric value. Examples: `42`, `98.6`
    * **Enum** - A value from a predefined list. Examples: `"Yes"`, `"No"`, `"Maybe"`
    * **Boolean** - True or false.

    Click **Save** to add variable.

    <Frame>
      <img />
    </Frame>

    Add more variables as per requirement
  </Step>

  <Step title="Save the Extract Dynamic Variable Tool">
    Click the save button

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Update prompt for function">
    It’s best to include in the prompt explicitly when is the best time to invoke the extract variable function. For example:

    ```
    When user states his name and phone number, please extract the information by calling the `extract_user_details` function.
    ```
  </Step>
</Steps>


# Function Calling Overview
Source: https://docs.retellai.com/build/single-multi-prompt/function-calling

Enable your AI agent to perform actions like transfers, bookings, and API integrations through function calling

## Introduction

Function calling transforms your AI agent from a conversational interface into an action-oriented assistant. By connecting your agent to functions, you enable it to interact with external systems, manage call flows, and perform real-world tasks.

## Common Use Cases

Function calling enables your agent to:

### Call Management

* **Transfer calls**: Route to human agents or other departments
* **End calls**: Gracefully terminate conversations
* **Send DTMF tones**: Navigate phone menus

### Business Operations

* **Book appointments**: Integrate with scheduling systems
* **Check availability**: Query calendars or inventory
* **Process orders**: Create, modify, or cancel orders

### Data Integration

* **Retrieve information**: Pull data from CRMs, databases, or APIs
* **Update records**: Modify customer information or case details
* **Send notifications**: Trigger emails, SMS, or push notifications

## How Function Calling Works

### The Process

1. **Agent Decision**: Based on the conversation context, the LLM determines when a function is needed
2. **Parameter Extraction**: The agent extracts required information from the conversation
3. **Function Execution**: Retell calls your function with the extracted parameters
4. **Response Handling**: The function result is processed and incorporated into the conversation

### Technical Overview

Function calling uses structured JSON to communicate between the LLM and your systems:

```json theme={null}
{
  "function": "book_appointment",
  "arguments": {
    "date": "2024-03-15",
    "time": "14:00",
    "customer_name": "John Smith"
  }
}
```

### Additional Resources

* [OpenAI's Function Calling Guide](https://platform.openai.com/docs/guides/function-calling): Technical deep dive
* [Function Calling Tutorial](https://semaphoreci.com/blog/function-calling): Step-by-step implementation guide

## Configuring Tool Calls

### Dashboard Configuration

Access and manage tools in the agent detail page under the "Functions" section.

<Frame>
  <img alt="Functions section in dashboard" />
</Frame>

## Available Function Types

### 1. Pre-built Functions

Retell provides ready-to-use functions for common scenarios:

| Function                                                      | Purpose                           | Common Use Cases                             |
| ------------------------------------------------------------- | --------------------------------- | -------------------------------------------- |
| [**End Call**](/build/single-multi-prompt/end-call)           | Terminate conversation gracefully | After completing tasks, when caller requests |
| [**Transfer Call**](/build/single-multi-prompt/transfer-call) | Route to human agents             | Escalation, department routing               |
| [**Press Digits**](/build/single-multi-prompt/press-digit)    | Send DTMF tones                   | Navigate IVR systems, enter codes            |
| [**Check Availability**](/build/check-availability)           | Query available time slots        | Appointment scheduling                       |
| [**Book Calendar**](/build/book-calendar)                     | Create calendar events            | Confirm appointments, meetings               |
| [**Send SMS**](/build/single-multi-prompt/send-sms)           | Send text messages                | Confirmations, follow-ups                    |

### 2. Custom Functions

Create your own functions to:

* **Integrate with your APIs**: Connect to CRM, ERP, or custom systems
* **Execute business logic**: Validate data, calculate prices, check inventory
* **Trigger workflows**: Start processes in other systems

#### Custom Function Features

* **Flexible parameters**: Define any input structure
* **Async execution**: Run in background without blocking conversation
* **Error handling**: Graceful fallbacks for failures
* **Response control**: Customize what the agent says during/after execution

[Learn more about custom functions →](/build/single-multi-prompt/custom-function)

### 3. Code Tool

Run JavaScript code directly in Retell's sandbox without setting up an external server. Useful for:

* **Data transformation**: Format, combine, or compute values from dynamic variables
* **Simple API calls**: Fetch data using the built-in `fetch()` function
* **Logic and calculations**: Implement conditional logic, math, or string operations

[Learn more about Code Tool →](/build/single-multi-prompt/code-tool)

## Video Tutorial

<iframe title="YouTube video player" />

### Additional Resources

* [Community Templates](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope): Real-world function examples
* [API Reference](/api-references/create-agent): Technical documentation
* [Best Practices](/build/prompt-engineering-guide): Writing effective function prompts


# MCP
Source: https://docs.retellai.com/build/single-multi-prompt/mcp



MCP allow you to extend your agent's capabilities by integrating external MCPs and utilize MCP tools.

## Steps

<Steps>
  <Step title="Add MCP">
    To use MCP tools, you first need to connect your agent to the MCP server. This step will allow you to authenticate and set up the connection.

    Click on + Add MCP

    <Frame>
      <img />
    </Frame>

    Add MCP Configuration

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set request headers (optional)">
    You can define custom headers to include with the request Retell sends to your MCP Server.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set query parameters (optional)">
    You can define query parameters to include in the request URL that Retell appends to your MCP Server Endpoint.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Select Tool">
    Select the MCP tool from the list of tools available

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Set response variables (optional)">
    Extract values from the MCP tool response and save them as <strong>dynamic variables</strong> for use later in the conversation.

    For example, you can extract a user’s name from the response and reference it later using <code>\{\{user\_name}}</code>.

    Example response body

    ```javascript theme={null}
    {
      "properties": {
        "user": {
          "name": "John Doe",
          "age": 26
        }
      }
    }
    ```

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Save the MCP Tool">
    Click the save button
  </Step>

  <Step title="Update prompt for function">
    It’s best to include in the prompt explicitly when is the best time to invoke the mcp tool. For example:

    ```
    When user states his name and phone number, please call tool `verify_user` function.
    ```
  </Step>
</Steps>


# Press digit (IVR navigation)
Source: https://docs.retellai.com/build/single-multi-prompt/press-digit

Enable Retell AI agents to navigate IVR systems using DTMF input.

When making outbound phone calls, voice agents often encounter IVR (Interactive Voice Response) systems. The agent needs to navigate the IVR to reach the right department or person, or to enter necessary information.

There are two types of IVR systems:

* **Audio input IVR**: Accepts spoken responses. Your agent can navigate these through standard prompting.
* **DTMF input IVR**: Requires pressing digits on the phone keypad (Dual-Tone Multi-Frequency signals).

This guide shows you how to configure your agent to navigate DTMF-based IVR systems by pressing digits.

***

## Steps

<Steps>
  <Step title="Add a Press Digit Tool">
    Give your agent the ability to press digits. The tool description is optional—you can specify when and what digits to press if desired.

    <img />
  </Step>

  <Step title="Add Navigation Prompts">
    Provide clear instructions on when and what digits to press. Include preferred keywords/phrases, keywords to avoid, and guidance for uncertain situations.

    **Example prompt:**

    ```
        ## IVR Navigation
        When interacting with automated systems, menus, or IVR prompts:

        Your goal is to reach the scheduling or appointments department.

        Preferred navigation keywords:
        • Scheduling
        • Appointments
        • New patients
        • Front desk

        Avoid:
        • Billing
        • Referrals
        • Medical records
        • Clinical departments

        If you are unsure which IVR option is correct:
        Choose the option most closely related to scheduling or appointments.
    ```

    **Alternative approach:** If you know the exact digit sequence beforehand, you can provide direct instructions:

    ```
        Press digit 1 to reach the support department.
    ```
  </Step>

  <Step title="Add Interaction Rules">
    Provide detailed instructions on when to press digits and how to handle edge cases, such as reaching the wrong person or needing to hang up.

    **Example prompt:**

    ```
        ## IVR Interaction Rules
        1) If the IVR allows you to speak a department name or short phrase:
            - Speak the appropriate department name clearly.

        2) If the IVR explicitly instructs you to press a number:
           - Use the press_digit function with the instructed digit.

        3) If the IVR does not accept speech and requires numeric input:
           - Use the press_digit function to select the best option.

        4) If the IVR indicates that you have reached the wrong company:
           - Immediately call end_call.

        5) If you are transferred:
           - Wait silently or respond with NO_RESPONSE_NEEDED if prompted to hold.
           - Resume navigation or follow the live agent flow once connected.
    ```
  </Step>

  <Step title="Extract IVR Post-Call Data (Optional)">
    Extract IVR navigation data for deeper insights. Below are field-by-field extraction prompts you can add in your agent's Post-Call Data Extraction settings:

    <img />

    <AccordionGroup>
      <Accordion title="hit_ivr (boolean)">
        Was an IVR or automated phone system encountered at any point before reaching a human? Count menus, "press 1", speech menus, automated routing, or virtual assistants as IVR. Do NOT count hold music after a human answers. Output ONLY true or false.
      </Accordion>

      <Accordion title="reached_human (boolean)">
        Did the caller speak with a real human staff member at any point during the call (not an automated system, recording, voicemail, or virtual assistant)? Output ONLY true or false.
      </Accordion>

      <Accordion title="ivr_loop (boolean)">
        Did the IVR appear to loop or repeat the same menu/prompt due to misunderstanding or invalid input (e.g., repeated "I'm sorry, I didn't get that" or returning to the main menu multiple times)? Output ONLY true or false.
      </Accordion>

      <Accordion title="ivr_type (enum)">
        **Allowed values:** `none` | `basic_menu` | `speech_ivr` | `voicemail_greeting_only` | `after_hours_message_only`

        Classify the type of automated system encountered:

        * **none**: no automation, human answered directly
        * **basic\_menu**: "press 1/2/3" style DTMF menu
        * **speech\_ivr**: system asks spoken questions like "tell me why you're calling" and responds conversationally
        * **voicemail\_greeting\_only**: immediately reached voicemail greeting/leave-a-message flow (no menus)
        * **after\_hours\_message\_only**: only an after-hours closed message (may mention hours), without offering routing to staff
      </Accordion>

      <Accordion title="ivr_outcome (enum)">
        **Allowed values:** `reached_human` | `left_voicemail` | `hung_up` | `blocked_by_ivr` | `callback_required` | `transferred` | `ivr_loop_detected` | `invalid_extension` | `after_hours_info_only`

        What was the final outcome of the IVR/automated navigation portion of the call?

        * **reached\_human**: successfully got to a human
        * **left\_voicemail**: reached voicemail and a message was left or the voicemail prompt occurred as the end state
        * **hung\_up**: call ended before any resolution (caller or system disconnected)
        * **blocked\_by\_ivr**: could not proceed due to IVR requirements or no matching menu option
        * **callback\_required**: system instructed to call back later or offered callback as the only option
        * **transferred**: IVR transferred to a line/department (even if later hold)
        * **ivr\_loop\_detected**: looping prevented progress
        * **invalid\_extension**: extension entry failed (invalid/not recognized)
        * **after\_hours\_info\_only**: ended at after-hours info message with no human reached
      </Accordion>

      <Accordion title="ivr_steps_count (number)">
        How many distinct IVR steps occurred (menu prompts or bot questions that required an input/response) before reaching a human or ending? Output ONLY an integer. If none, output 0.
      </Accordion>

      <Accordion title="ivr_retries_count (number)">
        How many times did the IVR/bot request the same input again or say it didn't understand (e.g., "please repeat", "invalid entry", returning to same menu)? Output ONLY an integer. If none, output 0.
      </Accordion>

      <Accordion title="ivr_path (text)">
        Summarize the IVR navigation path as a breadcrumb using > separators, capturing the main menu choices or intents.

        **Example:** `Main Menu > Providers > Authorizations > Hold`
      </Accordion>

      <Accordion title="ivr_notes (short text)">
        In 1–2 sentences, summarize the key IVR insights that matter operationally (e.g., required identifiers, department options heard, barriers like "portal only", after-hours).
      </Accordion>

      <Accordion title="ivr_tree_text (multiline text)">
        Create a concise step-by-step IVR tree in numbered lines. Each line must be:

        `N. Prompt: "<summary>" | Action: "<pressed/said>" | Result: "<next state>"`.

        Include only steps that occurred.
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="Test Your Configuration">
    After saving your agent, test it by:

    * Placing an outbound call to a number with an IVR system, or
    * Calling yourself and mimicking an IVR system by saying phrases like "Press 1 for customer service"
  </Step>
</Steps>


# Single/Multi Prompt Agent Overview
Source: https://docs.retellai.com/build/single-multi-prompt/prompt-overview

Choose between single or multi-prompt structures to build AI agents with the right balance of simplicity and control

## Introduction

Retell offers two prompt-based approaches for building conversational agents, each suited to different complexity levels and use cases. Understanding when to use each approach is crucial for creating effective AI phone agents.

## Agent Architecture Options

<Frame>
  <img alt="Create Agent Interface" />
</Frame>

1. Single Prompt: Design your agent with one comprehensive prompt
2. Multi-Prompt Tree: Structure your agent with multiple organized prompts

### Single Prompt Agent

A single prompt agent uses one comprehensive prompt to define all agent behaviors, making it the simplest approach to get started.

<Frame>
  <img alt="Single prompt configuration interface showing a unified prompt field" />
</Frame>

#### When to Use Single Prompt

✅ **Best for:**

* Simple, straightforward conversations
* Quick prototypes and testing
* Agents with 1-3 functions
* Linear conversation flows

#### Limitations at Scale

As complexity increases, single prompt agents may experience:

1. **Behavioral Drift**: Agent deviates from instructions in edge cases
2. **Function Calling Issues**: Unreliable tool usage with multiple functions
3. **Maintenance Challenges**: Large prompts become difficult to debug and update
4. **Context Confusion**: Agent struggles to track conversation state

<Note>
  Consider using conversation flow agent or multi-prompt agent when your single prompt exceeds 1000 words or uses more than 5 functions.
</Note>

### Multi-Prompt Agent

Multi-prompt agents organize conversations into a structured tree of states, each with its own focused prompt and behavior.

<Frame>
  <img alt="Multi-prompt tree structure showing connected conversation states" />
</Frame>

#### Key Features

Each state in a multi-prompt agent includes:

* **Focused Prompt**: Specific instructions for that conversation phase
* **State-Specific Functions**: Only relevant tools available in each state
* **Transition Logic**: Clear conditions for moving between states
* **Context Preservation**: Variables and information flow between states

#### Real-World Example: Lead Qualification

<Frame>
  <img alt="Lead qualification template showing two-state structure" />
</Frame>

This template demonstrates effective state separation:

**State 1: Lead Qualification**

* Gather customer information
* Validate requirements
* No appointment booking functions available

**State 2: Appointment Scheduling**

* Only accessible after qualification complete
* Booking functions enabled
* Context from qualification available

#### Benefits of Multi-Prompt Structure

1. **Predictable Behavior**: Each state has a clear, focused purpose
2. **Easier Debugging**: Issues isolated to specific states
3. **Better Function Control**: Tools available only when appropriate
4. **Scalable Design**: Add new states without affecting existing ones
5. **Team Collaboration**: Different team members can work on different states

<Tip>
  Start with our templates to see multi-prompt best practices in action, then customize for your use case.
</Tip>


# Send SMS
Source: https://docs.retellai.com/build/single-multi-prompt/send-sms



This tool is used to send an SMS during a phone call. You can send to the caller's number or a different number.

<Note> This tool only works for phone numbers that have SMS enabled, or when using an SMS-approved Retell number. Read more about [enabling SMS](/deploy/enable-sms). </Note>

<Tip>Agents can also **receive SMS during an active call** and understand the content, including text, images, audio, and video. This works out of the box for Retell Twilio numbers, and for custom telephony numbers that passed A2P applications. Read more at [Receive SMS during call](/deploy/enable-sms#receive-sms-during-call).</Tip>

<img />

## Choose where to send from

<Frame>
  <img alt="Send In-Call SMS tool configuration showing SMS-approved Retell number and agent's associated number options" />
</Frame>

You can choose one of two options for the sending number:

* **SMS-approved Retell number**: Send from Retell's pool of numbers that are already approved for SMS. This bypasses the A2P application process entirely. The message content is a **preset template provided by Retell** — you cannot customize the text or use a prompt.
* **Agent's associated number**: Send from the phone number bound to the agent. This requires your number to have SMS enabled through the [A2P application](/deploy/enable-sms#enable-sms-capabilities).

## Configure SMS content

* **When sending from the agent's associated number**: You can write a prompt to let the agent infer the SMS content, or use static SMS content. Dynamic variables are supported for static SMS content.
* **When sending from an SMS-approved Retell number**: The message is a preset template provided by Retell. You cannot edit the content.

## Configure SMS destination

By default, the SMS is sent to the caller's number. You can also choose to send to a different number — either a static number or a dynamic variable (e.g. `{{customer_phone}}`).

## Talk while waiting

Enable this option to have the agent say a short phrase while the SMS is being sent. You can configure the message as a prompt or a static sentence.

## Speak after sending message

Enable this option to have the agent speak after the SMS has been sent. This is useful for confirming to the user that the message was delivered.


# Agent Transfer
Source: https://docs.retellai.com/build/single-multi-prompt/transfer-agent



In advanced call flows, it's common to switch the handling agent, transferring the conversation from one AI agent to another. **Agent Transfer** (also known as **Agent Swap**) enables you to modularize tasks and re-use specialized agents without relying on [traditional phone-based transfers](/build/single-multi-prompt/transfer-call). Examples include:

* Transferring from a front-desk agent to an appointment-booking agent based on task.
* Transferring from an agent speaking one language to another agent handling a different language, based on user preference.

## Why Use Agent Transfer Instead of Call Transfer?

Compared to transferring to another agent using [transfer call](/build/single-multi-prompt/transfer-call), **Agent Transfer** offers significant advantages:

* **Lower Latency**: The transition between agents is near-instant, much lower than transfer call.
* **Better Reliability**: No need to create a new phone call, avoiding potential telephony failures.
* **No Handoff Message Needed**: The destination agent has access to the full conversation history, eliminating the need for adding hand-off messages or repeated customer questions.
* **No Separate Numbers for Agents**: Agents receiving transfers don’t need their own phone numbers — one number is all you need, no matter how many agents you transfer to.

## Transfer Settings Behavior

The following settings of the first agent will be used throughout the call:

* optInSignedUrl
* optOutSensitiveDataStorage
* webHookUrl

All other settings — such as language, voice, and voiceModel — will reflect the currently active agent.

## Steps

<Steps>
  <Step title="Add Agent Transfer Tool">
    Click Add in the tools section and select "Agent Transfer" from the dropdown menu.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Details">
    You can configure the following main settings:

    * **Transfer agent**: the ID and version of a specific agent to transfer to. You can select the latest version as well.
    * **Speak during execution and messages**: if the agent should speak something while performing the transfer.
    * **Post call analysis setting**: for post-call analysis, only extract dynamic variables for the transferred agent, or both agents.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Update the Prompt to Enable Agent Transfer">
    Ensure the AI agent knows when and why to trigger the agent transfer. Add clear instructions in the prompt such as:

    * `"If the user asks to book an appointment, use the agent_transfer tool to transfer to the Appointment Agent."`

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Test and Debug">
    You can test agent transfer both in web call and playground.

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>


# Transfer call
Source: https://docs.retellai.com/build/single-multi-prompt/transfer-call



<Warning>
  This feature only works during phone calls instead of web calls. It's available for Retell numbers and imported numbers.
</Warning>

It is common in call operation to transfer the call to another human agent or another AI agent.

<Steps>
  <Step title="Add Transfer Call Tool">
    Click "+ Add" in the tools section and select "Transfer Call" from the dropdown menu.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Setup Transfer To Target">
    Set transfer number to be either:

    * a number in e.164 format, or a SIP URI in the format of `sip:username@domain` (e.g. `sip:user@retellai.com`).
    * [dynamic variable](/build/dynamic-variables) that gets substituted at runtime
    * (Optional) if your transfer destination is not in e.164 format then you can choose to keep the input as is by choosing raw format. This only applies when you are using custom telephony and does not apply when you are using Retell Telephony

    <Frame>
      <img />
    </Frame>

    Set the transfer number extension if needed. Extension must be 0-9, '\*', '#' (E.g. 123#)
  </Step>

  <Step title="Update the Prompt">
    Enhance the agent's understanding by incorporating the transfer call conditions into the prompt. Include specific instructions such as:

    "If the user is angry or frustrated, use the transfer\_call tool to transfer the conversation to a human agent."

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Transfer Type">
    Choose between cold transfer or warm transfer:

    * **Cold transfer**: The call is transferred to a destination number and that's it.
    * **Warm transfer**: After the call is transferred to the destination number, the AI agent can attempt to detect if the other side is human, leave private messages that are not heard by user, do a three-way introduce, etc. (more details in Step 5).
  </Step>

  <Step title="Configure Caller ID (Optional)">
    You can configure which caller id shows up to the transfer destination:

    1. **Retell Agent's number**: The transfer destination will see the Retell agent's number

    2. **User's Number**: The transfer destination will see the number of the user. Please note that the telephony provider must support caller id override for this feature to work.
       * For warm transfer, it's using SIP DIAL, and we are setting `from` and `P-Asserted-Identity` headers to the user's number.
       * For cold transfer, it's using SIP REFER, and it's up to the telephony provider to support caller id override for SIP REFER.
       * Retell Twilio numbers support showing user's number on both warm and cold transfer, Retell Telnyx numbers only support this when using SIP REFER via cold transfer.
       * If caller id override is not supported, the transfer would fail.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Configure Warm Transfer Specific Settings">
    For warm transfers, you can configure the following settings:

    * **On-hold music**: The audio played to the caller while they are on hold. The default is a standard ringtone.
    * **Navigate IVR**: Provide an prompt to help you navigate if the transfer target is an IVR system.
    * **Enable human detection**: When enabled, the agent will check if a human is present after the transfer target answers. The original caller will only be connected once a human is detected.
    * **Auto-greet**: If enabled, the agent will immediately say “Hello” when the transfer target picks up. This encourages a response, increasing the likelihood of detecting a human.
    * **Agent detection timeout**: The maximum amount of time the AI agent will wait to determine whether the transfer target is a human. The caller is connected only if human detection succeeds within this timeframe. Otherwise, the transfer is marked as failed. The default timeout is 30 seconds.
    * **Whisper message (optional)**: A message spoken privately to the transfer target before connecting them to the original caller.
    * **Three-way message (optional)**: A message spoken to both the transfer target and the original caller once the connection is established.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Add Custom SIP Headers (Optional)">
    Add custom SIP headers for outbound calls.  These headers are forwarded to your SIP provider on the SIP INVITE and can be used for custom routing, tagging, or metadata.

    <Warning>Custom SIP headers are preserved only when transferring the call directly to a SIP endpoint. They may be stripped if you are transferring the call to a PSTN number.</Warning>

    <code>All header names must start with `X-` or must be `User-To-User` (case insensitive)</code>

    <br />

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>


# Build a multi-prompt agent
Source: https://docs.retellai.com/build/single-multi-prompt/write-multi-prompt



<Frame>
  <img alt="Multi Prompt Agent" />
</Frame>

<Steps>
  <Step title="Break down the conversation into steps">
    In each step, you can define a prompt.
  </Step>

  <Step title="Define state transition logic">
    Just like in the "Lead qualification" template, you can have this prompt to define when to transition to the next step like if users say "yes" to the question, transition to `your_next_state` state.

    ```
    7. Ask if user is interested in an in person tour.
     - if yes, transition to schedule_tour.
     - if no or hesitant, call function end_call to hang up politely and say will reach out if any other interesting properties pop up.
    ```
  </Step>

  <Step title="Define when to call the function">
    Just like in the "Lead qualification" template, you can have this prompt to define when to call the function like call the `your_function_name` function to book the appointment.

    ```
    3. Confirm the date, time, and timezone selected by user: "Just to confirm, you want to book the appointment at ...". Make sure this is a time from the available slots.
    4. Once confirmed, call function book_appointment to book the appointment.
    ```
  </Step>
</Steps>

### Video tutorial

<iframe title="YouTube video player" />

See community templates in [docs](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope)


# Write a single prompt
Source: https://docs.retellai.com/build/single-multi-prompt/write-single-prompt



Prompt Engineering might be the most important part of your agent, it can make or break your agent.
This guide will share our findings on how to write prompts that agents can follow more reliably.

This guide is a work in progress and will be updated as we learn more.
If you have any suggestions or feedback, please let us know.

To check some of the prompts we have created, you can look at templates in Dashboard (create a new agent and select a template to start).

### Sectional Prompts

When writing prompts, it is important to break down the system prompts into smaller sections, where each section has its
focus, like identity, style, guideline, task & goals. This has a couple of benefits:

* reusable
* easier to maintain
* easier for LLM to understand

```
## Identify
You are a friendly AI assistant for Retell AI. ....

## Style Guardrails
Be concise: ...
Be conversational: ...
...

## Response Guideline
Return dates in their spoken forms: ...
Ask up to one question at a time: ...
...

## Task
1. Greet the user
...

```

### Write Task as Steps

During a call, if you want agent to follow a specific procedure to lead the conversation, we recommend writing the task as steps.
This will help LLM understand what to ask at each step and how to proceed. You can have some logic in the steps as well. This also
ensures agent does not pack all questions in one go.

```
## Task
1. Ask for user's name.
2. Ask if user needs a refund, need a replacement, or just retriving information.
  - if user needs a refund, transition to refund state.
  - if user needs a replacement, transition to replacement state.
3. If user is just retriving information, ask for the order number.
...

```

If you noticed that the agent is still not stopping at the right time, or you need to go through some steps and not stop
at each step, you can write it like the following
by adding `wait for user response` to be more explicit:

```
## Task
1. Inform user why you are calling.
2. Ask for user's name.

wait for user response

3. Ask if user needs a refund, need a replacement, or just retriving information.

wait for user response
  - if user needs a refund, transition to refund state.
  - if user needs a replacement, transition to replacement state.


4. Ask for the order number.

wait for user response
...

```

### Prompt Engineer Video Guidance

<iframe title="YouTube video player" />

See community templates in [docs](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope)


# Apply for branded call
Source: https://docs.retellai.com/build/telephony/branded-call



*Only available for U.S. numbers at this time*

Branded Call allows you to display your business name instead of just a phone number when making calls to your customers. This feature increases trust and call answer rates by helping recipients instantly identify your business.

<Frame>
  <img alt="Apply for branded call" />
</Frame>

> **Important:** Without a verified phone number, your calls may be marked as "Spam Likely". We strongly recommend enabling [verified caller ID](/build/telephony/verified-phone) to ensure your business name displays correctly and to maximize the benefits of branded call.

## Setup Process

### Step 1: Create a Business Profile

Follow the guide in [Business Profile](/build/telephony/business-profile) to create and verify your business profile.

### Step 2: Apply for Branded Call

1. Navigate to the Branded Call section
2. Select your verified business profile
3. Enter your desired business name display

<Frame>
  <img alt="Apply for branded call" />
</Frame>

Please allow 1-2 weeks for your application to be processed.

## Business Name Requirements

Different carriers have varying character limits for business names:

* T-Mobile: Up to 32 characters
* AT\&T: Up to 32 characters
* Verizon: Up to 15 characters

You can provide both a short name (for carriers with lower character limits) and a long name (for carriers that support longer displays).


# Handle application rejection
Source: https://docs.retellai.com/build/telephony/branded-call-rejection



We will review your business profile, phone verification, or branded call application. If the application is rejected for any reason, you will receive an email notification.

<Frame>
  <img alt="Rejection status" />
</Frame>

<Steps>
  <Step title="Check Rejection Status">
    Go to your phone detail page where you'll see your "Verified Phone Number" or "Branded Call" showing a "Rejected" status.

    <Frame>
      <img alt="Rejection status" />
    </Frame>
  </Step>

  <Step title="Review Rejection Reason">
    Click to view the detailed reason for rejection.

    <Frame>
      <img alt="Rejection details" />
    </Frame>
  </Step>

  <Step title="Check Business Profile">
    If your business profile was rejected, click on the business profile details to understand why.

    <Frame>
      <img alt="Business profile rejection" />
    </Frame>
  </Step>

  <Step title="Resubmit Application">
    After addressing the rejection reasons, you can resubmit your application through the dashboard.
  </Step>
</Steps>


# Add a business profile
Source: https://docs.retellai.com/build/telephony/business-profile



Before applying for premium services like verified phone numbers or branded calls, you must first create and verify your business profile. This guide will walk you through the process.

### Step 1: Access Business Profile Setup

1. Navigate to any premium service (e.g., Verified Phone Number or Branded Call)
2. Look for the Business Profile section in the setup process

<Frame>
  <img alt="Add Business Profile" />
</Frame>

### Step 2: Complete Business Profile Form

Fill in all required business information across both sections of the form:

<Frame>
  <img alt="Business Profile Form Part 1" />
</Frame>

<Frame>
  <img alt="Business Profile Form Part 2" />
</Frame>

#### Important Requirements:

* **Business Registration**: Enter the exact registration number as it appears on your official documents
* **Business Address**: Provide your current, verified business address
* **Contact Number**: Use a physical phone line (VoIP numbers are not accepted)
* **Website**: Ensure your website's content accurately reflects your business name and operations

### Step 3: Submit and Continue

1. Click "Save" to submit your business profile
2. Click "Next" to proceed with your service application

<Frame>
  <img alt="Continue to Service Setup" />
</Frame>


# Spam Likely Overview
Source: https://docs.retellai.com/build/telephony/call_efficiency_overview



<div>
  <Frame>
    <img alt="Spam Likely" />
  </Frame>

  <Frame>
    <img alt="Apply for branded call" />
  </Frame>
</div>

Phone carriers may mark certain phone numbers as “Spam Likely". This would lead to your outbound calls to have a low call pickup rate, and can sometimes lead to telephony providers banning your number / account.

## Check whether your number is marked as spam likely

Check your outbound call log to see if the call was not connected due to SIP error code 608. If that's the case, that means it's rejected due to marked as spam likely. But it's not guaranteed that all calls rejected with spam likely will be marked as error code 608.

There are a couple of external API / services that can help you check if your number is marked as spam likely. This is not a perfect match as each carrier might have their own rules and database, but you can use it as a reference:

* [Nomorobo](https://www.nomorobo.com/): can use the app or use the API to check against its database to see if the number is marked as spam likely.
* [IPQualityScore](https://www.ipqualityscore.com/phone-number-validator): can check the phone number reputation score.

## Actions you can take

Retell provides two services to improve your call pickup rate:

1. **[Verified Phone](/build/telephony/verified-phone)**: Retell will register your number with the phone carrier, which will not be marked as spam by carriers.
2. **[Branded Call](/build/telephony/branded-call)**: Callee will see your number as your business name, instead of the generic Retell number.

## iOS 26 Call Screening

iPhones on iOS 26 may deploy a [call screening feature](https://support.apple.com/guide/iphone/screen-and-block-calls-iphe4b3f7823/ios). At the beginning of the call, Siri will ask unknown numbers to provide their name and reason for calling.
To pass this screen, enhance your agent prompt to construct a smooth response. For example:

```
## FAQ
Q: Hi, if you record your name and reason for calling, I'll see if this person is available
A: In one sentence, introduce yourself and explain why you are calling. <wait for response>
```

<div>
  <Frame>
    <img alt="iOS Call Screen" />
  </Frame>
</div>


# Stopping caller ID service
Source: https://docs.retellai.com/build/telephony/delete-service



You can stop an active caller ID service at any time. These services — Branded Calls and Verified Phone Numbers — are add-ons layered on top of your underlying telephony. **Stopping them does not interrupt calls.** Your agents will continue making and receiving calls; only the associated caller ID enhancement or number verification will be removed.

<Frame>
  <img alt="Delete service" />
</Frame>

## What Gets Removed

* **Branded Calls** — your branded caller ID will no longer appear on the recipient's screen. Calls will still connect, but will present as a standard unbranded call.
* **Verified Phone Numbers** — your number's spam remediation registration is removed. The number may begin appearing as "Spam Risk" or "Scam Likely" on recipient devices until re-registered.

## Important Billing Information

Please note the following billing implications when stopping services.

### Branded Calls

Billing continues until the end of your current billing cycle. You will retain branded caller ID display for the remainder of the paid period even after initiating the stop.

### Verified Phone Numbers

Billing stops immediately upon service deletion. You will only be charged for the portion of the billing cycle the service was active.

<Note>
  If you plan to re-register a Verified Phone Number in the future, be aware that the re-registration process can take time. Your number may be flagged as spam in the interim.
</Note>


# Set & parse custom SIP headers
Source: https://docs.retellai.com/build/telephony/sip-headers



<Note>Custom SIP headers are used heavily in telephony SIP world to pass information around. It's only available for phone calls. Right now we support receiving SIP headers for inbound calls, sending SIP headers for outbound calls and when initiating transfers.</Note>

Many SIP parsers and middleboxes assume 1024 bytes is a reasonable maximum for a header line and may reject or truncate longer headers if not explicitly configured to allow more.

## Parse custom SIP headers for inbound calls

For inbound calls, the custom SIP headers (headers that starts with `X-` or `x-`) are automatically received, extracted and available in the `call.custom_sip_headers`, it's also automatically added to your collection of [dynamic variables](/build/dynamic-variables), and you can access it within your agent by stripping the `X-` or `x-` prefix. There's no configuration needed for this feature.

For example, if this is the SIP header received for an inbound call:

```json theme={null}
{
  "X-test-header": "something",
  "X-another-header": "something else",
  "from": "1234567890"
  "to": "0987654321"
}
```

Then here's your `call.custom_sip_headers` field, and they will be added to your dynamic variables.

```json theme={null}
{
  "test-header": "something",
  "another-header": "something else",
}
```

If you have already specific dynamic variables with the same name for this inbound call, it will override the value received from the SIP header.

## Set custom SIP headers for outbound calls

<img />

For outbound calls, you can add custom SIP headers as needed. It must starts with `X-`.

## Set custom SIP headers for call transfers

For call transfers, you can also add custom SIP headers as needed. It must starts with `X-`.
You can use dynamic variable for your custom SIP header value, so you can pass information extracted from the call to the receiving party.

<Warning>For cold transfer with transferee number, it will use SIP REFER to transfer the call. Different telephony providers may or may NOT honor the custom SIP headers in the REFER request. Twilio for example, does not honor the custom SIP headers in the REFER request, so the sip headers you set in transfer call tool will not work for cold transfer with transferee number when using Twilio.</Warning>

If you are using:

* Conversation flow agents, check out [call transfer node](/build/conversation-flow/call-transfer-node#configure-transfer) for more details.
* Single / multi agent, check out [call transfer function](/build/single-multi-prompt/transfer-call) for more details.


# Apply for verified phone number
Source: https://docs.retellai.com/build/telephony/verified-phone



*Only available for U.S. numbers at this time*

Phone carriers may mark certain phone numbers as "Spam Likely", particularly when telephony providers like Twilio recycle previously used numbers. This can happen if a phone number was previously associated with spam activities before being reassigned.

<Frame>
  <img alt="Spam Likely" />
</Frame>

To ensure your Retell phone number maintains a trusted status and isn't flagged as spam, you can register it as a verified phone number.

### Step 1: Create a Business Profile

First, create a business profile by following our guide in [Business Profile](/build/telephony/business-profile).

### Step 2: Apply for Phone Number Verification

Once your business profile is set up, select it and submit your verification application through the dashboard.

<Frame>
  <img alt="Apply for verified phone number" />
</Frame>

### Step 3: Verification Approval

Once your phone number verification is approved, it will appear in the configuration screen for the selected number under the "Phone Numbers" tab with an "Active" status, indicating that your number is now verified and trusted.

<Frame>
  <img alt="Verified phone number with Active status" />
</Frame>

Please allow 1-2 weeks for your application to be processed.


# Balance between transcription accuracy and latency
Source: https://docs.retellai.com/build/transcription-mode

Guide on how to select the right transcription mode for your agent.

<Note> This guide only applies to cascading agents, if you are using speech to speech models, this feature does not apply. </Note>

Real time transcription is often a trade off between latency and accuracy. When relying on interim results, you get the lowest latency but with a higher chance of errors due to less context. When relying on results generated with more context, you risk waiting longer after the user stops speaking.

## Transcription modes

<img />

* optimize for speed: uses the latest interim results with a low endpointing setting for downstream processing.
* optimize for accuracy: uses the results with a higher endpointing setting for downstream processing, essentially waiting longer with more context to generate more accurate transcripts. It will incur \~200ms latency.

## Which mode to use?

From our benchmarking, we found that the `optimize for speed` mode and `optimize for accuracy` mode have similar WER (Word Error Rate). The difference mainly lies in capturing entities like numbers, dates. If your use case relies heavily on capturing these entities well, you should use the `optimize for accuracy` mode. Otherwise you can use the `optimize for speed` mode for best latency.


# Setup TTS fallback
Source: https://docs.retellai.com/build/tts-fallback

Guide to setup fallback voices for your agent.

<Note>
  If you are using a [platform voice](/build/platform-voices) or a standard Retell voice from the voice library, fallback is handled automatically — no additional setup is required. The steps below apply only if you are using a custom or third-party provider voice.
</Note>

There might be cases where the TTS provider is having outages or temporary issues, but the agents need to keep talking to the user on call. Thus fallback and retries here are necessary. Fallback will use a different voice provider.

Currently if no specific TTS fallback is setup, the agent will use the default fallback plan that's being setup:

* it will use the same gender voice as the original voice (if the original voice has a gender field)
* it will follow a default plan, to fallback to the next voice in the list, and if that voice is also not available, it will fallback to the next voice in the list.
* even if the original voice is back online, the agent will still continue to use the fallback to minimize the change of voice during the call.

## Setup your own TTS fallback

You can setup your own fallback plan, so that it sounds similar, and user would not notice the change.

Here you can add multiple fallback voices, each need to be using different TTS provider, and it cannot be using the same provider as the original voice.

<Frame>
  <img alt="TTS fallback voice configuration with multiple fallback providers" />
</Frame>


# TTS provider comparison
Source: https://docs.retellai.com/build/tts-provider-comparison

Choosing the best TTS provider for your use case.

When selecting a TTS provider, consider the trade-offs between spelling accuracy (pronouncing spelled-out words like "W - O - R - D"), voice naturalness, pacing/tone consistency, and accent support.

<Note>
  These observations are based on our internal testing. Results may vary depending on the specific voice, model, or language used.
</Note>

## Provider Overview

### ElevenLabs

* **Best for:** Most natural sounding; best support for niche accent needs (e.g., Australian English)
* **Consideration:** You may occasionally notice small pacing/tone quirks; less reliable for exact spelling

### Cartesia

* **Best for:** Natural sounding with stronger spelling than ElevenLabs
* **Consideration:** Pacing/tone can sometimes be less consistent than ElevenLabs; localization may be weaker for certain accents

### MiniMax

* **Best for:** Strongest spelling + most consistent tone (rarely has pacing/tone quirks); great for Asian languages
* **Consideration:** Voice sound can sometimes feel more robotic compared to other providers

## Rules of Thumb

* Need most natural sound → ElevenLabs (or Cartesia)
* Need spelling accuracy → MiniMax (or Cartesia)
* Need most consistent tone → MiniMax
* Need specific accents → any provider can work, but ElevenLabs tends to perform best for niche accents
* Using an Asian language → MiniMax


# Capture DTMF input from user
Source: https://docs.retellai.com/build/user-dtmf

Configure your AI agent to handle DTMF input from the user

There are times where user can provide information via DTMF (phone keypad presses) instead of voice. For example, when entering a PIN number, it might be easier for user to press keypad instead of speaking it aloud in public.

Currently DTMF input from user is captured and is taken into account when the agent is generating responses by default. So to set it up, you just need to prompt the agent to ask for the information via DTMF.

### DTMF Input Completion Options

The agent supports three methods for determining when DTMF input is complete:

* **Digit Limit (`ser_dtmf_options.digit_limit`)**\
  The maximum number of digits the user can enter. Once this limit is reached, input is considered complete.

* **Termination Key (`user_dtmf_options.termination_key`)**\
  A specific key (such as `#`, `*`, or any digit) that signals the end of input.

* **Timeout (`user_dtmf_options.timeout_ms`)**\
  The time in milliseconds to wait after the last digit is received before timing out. The timer resets with each new digit.

You can find these options under **Call Settings**.

<img />

Here's an example prompt:

```
Please enter your PIN number using the keypad. You can finish by pressing the pound key.
```

And the transcript would look like this:

<img />


# Choose a custom voice
Source: https://docs.retellai.com/build/voice

Customize your AI agent with community voices or train a voice clone for a unique sound.

If you find the existing voice doesn't meet your needs, you can add a custom voice. There's a limit of 100 custom voices per account. If you need more, please contact [support@retellai.com](mailto:support@retellai.com)

## Add Custom Voice

In the voice selector, you can click "Add custom voice" to search and add publicly available community voices.

<Frame>
  <img />
</Frame>

## Add Voice Clone

You can also add a voice clone by clicking "Add custom voice" in the voice selector.

<Steps>
  <Step title="Access Voice Clone Feature">
    Open the voice selector and click "Add custom voice".

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Train Your Voice Clone">
    Upload your voice recordings to train the voice clone.

    <Frame>
      <img />
    </Frame>
  </Step>
</Steps>


# A/B Testing
Source: https://docs.retellai.com/deploy/ab-testing

Split traffic between multiple agents for inbound and outbound calls and chats to run experiments

A/B testing lets you compare multiple agents or scripts by sending a percentage of traffic to each. You define a traffic split (for example, 80% to one agent and 20% to another) so you can test different prompts, voices, or flows without changing your main agent.

## Where A/B testing is available

A/B testing is supported for:

* **Inbound calls** — Calls received on a phone number
* **Outbound calls** — Calls made from a phone number
* **Inbound chats** — Incoming chat conversations
* **Outbound chats** — Chat sessions you initiate

## How it works

* **Multiple agents**: Bind or assign two or more agents to the same number or chat configuration.
* **Traffic split**: Set the percentage of traffic each agent receives (e.g., 80% / 20%). Traffic is distributed according to this split.
* **Use cases**: Test different scripts on marketing or support calls, try prompt or voice changes, or compare conversation flows in chat.

## Where to configure

**Phone numbers (calls):** On the phone number configuration page, the A/B Testing toggle appears next to the Call Agent field. Turn it on to bind multiple agents and set a traffic split. The screenshot below shows the control with A/B testing disabled.

<Frame>
  <img alt="Phone number configuration showing Call Agent dropdown and A/B Testing toggle in the off position" />
</Frame>

After you turn the toggle on, you can add one or more agents and set the traffic percentage for each (for example, one agent at 100% or a split such as 80% / 20%).

<Frame>
  <img alt="Call Agent section with A/B Testing on, showing one agent variant with 100% traffic and edit option" />
</Frame>

Click **Edit** to open the A/B Testing modal. There you choose which agents to use and set a weight (percentage) for each. You can add multiple agents and remove or adjust them; the weights must total 100%. Click **Deploy** to save.

<Frame>
  <img alt="A/B Testing modal with Agent and Weight columns, two agents at 50% each, Add button and Deploy/Cancel actions" />
</Frame>

After you click **Deploy**, the configuration is active. The Call Agent section shows each agent and its traffic percentage (for example, a 50/50 split). You can click **Edit** anytime to change the agents or weights.

<Frame>
  <img alt="Call Agent section with A/B Testing on, showing Agent A and Agent B each at 50% with Edit option" />
</Frame>

| Context                       | Configure in                                                                                                                                                                                                           |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Inbound calls**             | Number configuration: bind multiple agents to the number and set the traffic split. See [Receive calls](/deploy/inbound-call).                                                                                         |
| **Outbound calls**            | Number configuration: bind multiple agents for outbound and set the traffic split. See [Outbound calls](/deploy/outbound-call).                                                                                        |
| **Chat (inbound & outbound)** | Chat agent or widget configuration where you assign the chat agent; enable A/B testing and set the traffic split. See [Create Chat Completion](/deploy/create-chat-completion) and [Chat widget](/deploy/chat-widget). |

## View analytics by agent version

After you deploy an A/B test, you can compare performance by specific agent versions in the Analytics dashboard.

1. Open **Analytics** in the Retell dashboard.
2. Set a date range that covers your experiment period.
3. In the filter bar, click **Agent** (or click **Filter** and add **Agent**).
4. In the left panel, select the agent(s) used in your A/B test.
5. In the right panel, select the specific version(s) you want to analyze (for example, `Version 3` vs `Version 4` of the same agent).
6. Click **Save** to apply the filter.

All charts on the page will update to the selected agent-version scope, so you can compare metrics (such as call success rate, duration, and latency) for each variant.

For more details on Analytics, see [Get analytics insight](/features/analytics-dashboard).

## A/B testing vs dynamic agent selection

<Tabs>
  <Tab title="A/B testing">
    Use when you want a **random percentage-based split**. Traffic is distributed according to the percentages you set, with no per-call or per-chat logic.
  </Tab>

  <Tab title="Dynamic selection (webhook / API)">
    Use when you want to **choose the agent per call or per chat** based on caller, context, or other data. For inbound calls, use the [Inbound Call Webhook](/features/inbound-call-webhook). For outbound calls or chats, pass the agent (or other overrides) in the API when you create the call or chat.
  </Tab>
</Tabs>


# Amazon Connect
Source: https://docs.retellai.com/deploy/amazon-connect

Amazon Connect is a cloud-based contact center service from AWS that lets you set up and manage customer support call centers quickly.

<Note>
  Customers with enterprise or paid support plan can contact us via the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com) for step by step guidance to connect with your Amazon Connect infrastructure.
</Note>

Retell supports multiple integration patterns with Amazon Connect, catering to a variety of use cases. Every customer's setup is unique — and so is the way Amazon Connect integrates with Retell. Reach out to Retell support via [Customer Support Portal](https://support.retellai.com/) or [support@retellai.com](mailto:support@retellai.com) to discuss your specific Amazon Connect infrastructure and find the right integration approach for your needs.


# Avaya
Source: https://docs.retellai.com/deploy/avaya

A step by step guide to integrate Avaya Aura with Retell's SIP endpoints using Avaya SBCE as the border element to send and receive phone calls.

<Note>
  Customers with an enterprise or paid support plan can contact us via the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com) for step-by-step guidance to connect with your Avaya infrastructure.
</Note>

## Overview

This guide covers connecting **Avaya Aura** to Retell using **Avaya Session Border Controller for Enterprise (SBCE)** as the SIP border element between Retell and the Avaya core (Session Manager and Communication Manager).

**Architecture:**

```
Retell ↔ Avaya SBCE (B1 external) | (A1 internal) ↔ Session Manager ↔ Communication Manager
```

The SBCE handles topology hiding, codec interworking, and security policy between the external Retell SIP trunk and your internal Aura infrastructure. All configuration flows through **System Manager** (the central management UI for Aura).

**Retell SIP details:**

* SIP server URI: `sip.retellai.com`
* IP ranges: `18.98.16.120/30` (all regions), `143.223.88.0/21` (certain US traffic), `161.115.160.0/19` (certain US traffic)
* Recommended transport: TCP (also supports UDP and TLS/SRTP)
* Supported audio codecs: PCMU (G.711 µ-law), PCMA (G.711 A-law), G.722

**Official Avaya documentation references:**

* [Administering Avaya SBCE](https://documentation.avaya.com/bundle/AdministeringAvayaSBCERelease8/)
* [Administering Avaya Aura Session Manager](https://documentation.avaya.com/bundle/AdministeringSMRelease10/)
* [Administering Avaya Aura Communication Manager](https://documentation.avaya.com/bundle/AdministeringAuraCommunicationManager/)

***

<Steps>
  <Step title="Firewall Considerations">
    The SBCE has two network interfaces:

    * **A-side (external / untrusted)** — faces the internet / Retell.
    * **B-side (internal / trusted)** — faces Session Manager and Communication Manager.

    Apply the following rules on your perimeter firewall and on the SBCE's built-in packet filter.

    **Allow inbound to SBCE A-side from Retell IP ranges:**

    | CIDR Block         | Coverage           |
    | ------------------ | ------------------ |
    | `18.98.16.120/30`  | All regions        |
    | `143.223.88.0/21`  | Certain US traffic |
    | `161.115.160.0/19` | Certain US traffic |

    **Ports to open on the SBCE A-side (from/to Retell):**

    | Protocol  | Port       | Purpose                                 |
    | --------- | ---------- | --------------------------------------- |
    | TCP / UDP | 5060       | SIP signaling                           |
    | TCP       | 5061       | SIP over TLS (if using TLS transport)   |
    | UDP       | 1024–65535 | RTP / SRTP media (configurable on SBCE) |

    **Ports to open on the SBCE B-side (toward Session Manager):**

    | Protocol  | Port       | Purpose                                        |
    | --------- | ---------- | ---------------------------------------------- |
    | TCP / UDP | 5060       | SIP signaling to Session Manager               |
    | TCP       | 5061       | SIP/TLS to Session Manager (if TLS internally) |
    | UDP       | 1024–65535 | RTP media toward Communication Manager         |

    <Note>
      The SBCE's media port range is configurable under **SBCE** > **Global Profiles** > **Media Interface**. Match your firewall rules to whatever range you configure there.
    </Note>
  </Step>

  <Step title="Enable SIP Trunking on the Avaya System">
    Before creating the trunk, verify SIP trunking is enabled across the Aura stack.

    **On Communication Manager (via System Manager):**

    1. Log in to **Avaya System Manager** (`https://<smgr-ip>/SMGR`).
    2. Navigate to **Elements** > **Communication Manager** > select your CM instance > **System Parameters** > **Customer Options**.
    3. Confirm **SIP Trunking** is set to **y** (enabled). If not, contact your Avaya partner to activate the license.
    4. Confirm **Maximum Administered SIP Trunks** is set high enough to accommodate expected concurrent calls.

    **On Session Manager:**

    1. In System Manager, go to **Elements** > **Session Manager** > **System Status** > **Security Module Status**.
    2. Verify the Session Manager instance shows **Registered** and the SIP signaling service is active.
  </Step>

  <Step title="Configure the SBCE">
    All SBCE configuration is done through the **Avaya SBCE EMS (Element Management System)** web UI (`https://<sbce-ip>/`). Refer to [Administering Avaya SBCE](https://documentation.avaya.com/bundle/AdministeringAvayaSBCERelease8/) for full field-level reference.

    **1. Create Server Interworking Profiles**

    Server Interworking Profiles define how the SBCE adapts SIP behavior for each side of the trunk. You need one for the internal Avaya side and one for the external Retell (service provider) side.

    *Avaya-side profile:*

    1. Go to **Configuration Profiles** > **Server Interworking** > **Add**.
    2. Name it `Avaya`.
    3. Configure:
       * **SIPS Required**: unchecked (not required for this trunk type)
       * **Hold Support**: `None`
       * **Record Route**: `Both Sides`
       * **Include Endpoint IP for Context Lookup**: checked
       * **Extensions**: `Avaya`
       * **Has Remote SBC**: checked
       * **DTMF Support**: `None`
    4. Click **Finish**.

    *Retell (service provider) side profile:*

    1. Click **Add** again and name it `Service-Provider`.
    2. Configure:
       * **SIPS Required**: unchecked
       * **Delayed SDP Handling**: checked
       * **Record Route**: `Both Sides`
       * **Include Endpoint IP for Context Lookup**: checked
       * **Extensions**: `Avaya`
       * **DTMF Support**: `None`
         <Note>If your provider requires RFC 2833 DTMF relay or inband DTMF, change this to `RFC 2833` or `Inband` respectively. Check your provider's application note on [Avaya DevConnect](https://devconnect.avaya.com) for the correct value.</Note>
    3. Click **Finish**.

    ***

    **2. Add SIP Servers**

    SIP Servers represent the endpoints that the SBCE sends traffic to and receives traffic from.

    *Retell (service provider) server:*

    1. Go to **Configuration Profiles** > **Server Configuration** > **Add**.
    2. Name it `Service-Provider`.
    3. Configure:
       * **Server Type**: `Trunk Server`
       * **IP Address / FQDN**: `sip.retellai.com`
       * **Port**: `5060` (use `5061` if TLS)
       * **Transport**: `TCP` (recommended), `UDP`, or `TLS` — match what you configured on the Signaling Interface and what your firewall permits. TCP is preferred for reliability; use TLS if end-to-end encryption is required (see TLS step).
    4. Click **Next**. Leave authentication blank (IP-based trunk, no credentials required).
    5. On the **Heartbeat** tab:
       * Enable **SIP OPTIONS** ping, interval `30` seconds.
       * **From URI**: `sip@<sbce-b1-public-ip>` (your external interface's public IP).
       * **To URI**: `sip@sip.retellai.com`
    6. Click **Next**. Leave **Registration** and **Ping** defaults.
    7. Ensure **Enable Grooming** is unchecked (not applicable for non-TLS trunks; leave unchecked for TCP/UDP).
    8. Set **Interworking Profile** to `Service-Provider`.
    9. Click **Finish**.

    *Avaya Session Manager server:*

    1. Click **Add** and name it `Avaya`.
    2. Configure:
       * **Server Type**: `Call Server`
       * **IP Address**: your primary Session Manager IP (e.g., `10.x.x.x`)
       * **Port**: `5061`
       * **Transport**: `TLS`
    3. Click **Add** to include a secondary Session Manager IP with the same port and transport.
    4. Select the appropriate **TLS Client Profile** for your SBCE A1 interface (created during initial SBCE setup).
    5. Click **Next**. Skip authentication and registration — not required for Session Manager.
    6. Set **Interworking Profile** to `Avaya`.
    7. Click **Finish**.

    ***

    **3. Create Routing Profiles**

    Routing Profiles tell the SBCE where to forward calls for each direction.

    *Route to Retell (outbound):*

    1. Go to **Configuration Profiles** > **Routing** > **Add**.
    2. Name it `Route-to-Retell`.
    3. Click **Add**, set **Priority/Weight** to `1`, select **Server** `Service-Provider`.
    4. Click **Finish**.

    *Route to Session Manager (inbound):*

    1. Click **Add** and name it `Route-to-SessionManager`.
    2. Click **Add**, set priority `1` for your primary Session Manager and priority `2` for the secondary.
    3. Select the `Avaya` server for each entry.
    4. Click **Finish**.

    ***

    **4. Configure Topology Hiding**

    Topology Hiding rewrites SIP headers so internal IP addresses are not exposed externally, and so Session Manager receives the correct SIP domain.

    *Service Provider side:*

    1. Go to **Configuration Profiles** > **Topology Hiding** > **Add**.
    2. Name it `Service-Provider`.
    3. Set all header fields to `IP Domain`, leave all values as `Auto`.
    4. Click **Finish**.

    *Avaya side:*

    1. Click **Add** and name it `Avaya`.
    2. Set all header fields to `IP Domain`.
    3. For the following three fields, overwrite the value with your internal SIP domain (found in **System Manager** > **Routing** > **Domains**, e.g., `avaya.example.com`):
       * **To**
       * **From**
       * **Request Line**
    4. Click **Finish**.

    ***

    **5. Create Signaling Interfaces**

    Signaling Interfaces bind a specific IP address and port for SIP signaling on each SBCE network interface.

    *External interface (facing Retell):*

    1. Go to **Network & Flows** > **Network Management** > **Signaling Interface** > **Add**.
    2. Configure:
       * **Name**: `Service-Provider-External`
       * **IP Address**: your SBCE B1 (external) IP address
       * Enable only the port(s) matching your chosen transport:
         * **TCP Port**: `5060` — if using TCP
         * **UDP Port**: `5060` — if using UDP
         * **TLS Port**: `5061` — if using TLS (disable TCP and UDP)
       * Disable any ports not in use.
    3. Click **Finish**.

    *Internal interface (facing Session Manager):*

    1. Click **Add** and configure:
       * **Name**: `Avaya-Internal`
       * **IP Address**: your SBCE A1 (internal) IP address
       * Disable UDP and TCP ports — only TLS is used on the internal leg
       * **TLS Port**: `5061`
       * **TLS Profile**: select your SBCE A1 TLS client certificate profile
    2. Click **Finish**.

    ***

    **6. Create Media Interfaces**

    Media Interfaces bind the IP addresses used for RTP/SRTP on each leg.

    *External media interface:*

    1. Go to **Network & Flows** > **Network Management** > **Media Interface** > **Add**.
    2. Configure:
       * **Name**: `Service-Provider-External`
       * **IP Address**: your SBCE B1 (external) IP address
       * **Port Range**: default (e.g., `35000–40000`) — adjust to match your firewall rules
    3. Click **Finish**.

    *Internal media interface:*

    1. Click **Add** and configure:
       * **Name**: `Avaya-Internal`
       * **IP Address**: your SBCE A1 (internal) IP address
       * **Port Range**: default
    2. Click **Finish**.

    ***

    **7. Create Server Flows**

    Server Flows tie together the signaling interface, media interface, routing profile, topology hiding profile, and interworking profile for each call direction. You need two flows: one for calls coming in from Retell, and one for calls going out to Retell.

    Go to **Network & Flows** > **End-Point Flows** > **Server Flows**.

    *Flow 1 — Trunk Server (inbound from Retell → Session Manager):*

    | Field                       | Value                       |
    | --------------------------- | --------------------------- |
    | **Name**                    | `Trunk-Server`              |
    | **Server Configuration**    | `Service-Provider`          |
    | **Received Interface**      | `Service-Provider-External` |
    | **Signaling Interface**     | `Avaya-Internal`            |
    | **Media Interface**         | `Service-Provider-External` |
    | **Routing Profile**         | `Route-to-SessionManager`   |
    | **Topology Hiding Profile** | `Service-Provider`          |

    Click **Finish**.

    *Flow 2 — Call Server (outbound from Session Manager → Retell):*

    | Field                       | Value                       |
    | --------------------------- | --------------------------- |
    | **Name**                    | `Call-Server`               |
    | **Server Configuration**    | `Avaya`                     |
    | **Received Interface**      | `Avaya-Internal`            |
    | **Signaling Interface**     | `Service-Provider-External` |
    | **Media Interface**         | `Avaya-Internal`            |
    | **Routing Profile**         | `Route-to-Retell`           |
    | **Topology Hiding Profile** | `Avaya`                     |

    Click **Finish**.
  </Step>

  <Step title="Configure Session Manager — SIP Entities and Routing">
    Session Manager configuration is done through **System Manager** (`https://<smgr-ip>/SMGR`). Navigate to **Elements** > **Routing**.

    **1. Add a SIP Entity for the SBCE (if not already present)**

    1. Go to **SIP Entities** > **New**.
    2. Configure:
       * **Name**: `SBCE-Retell-Trunk`
       * **FQDN or IP**: SBCE A1 (internal) IP address — the interface facing Session Manager.
       * **Type**: `SIP Trunk`
       * **Adaptation**: leave blank unless header manipulation is needed.
       * **Location**: select your site location.
    3. Under **Port**, add:
       * **Port**: `5061`, **Protocol**: `TLS`
    4. Save.

    **2. Add an Entity Link between Session Manager and the SBCE**

    1. Go to **Entity Links** > **New**.
    2. Configure:
       * **Name**: `SM-to-SBCE-Retell`
       * **SIP Entity 1**: your Session Manager instance.
       * **Protocol**: `TLS`
       * **Port**: `5061`
       * **SIP Entity 2**: `SBCE-Retell-Trunk`.
       * **Connection Policy**: `Trusted`.
    3. Save.

    **3. Create a Routing Policy for Retell**

    1. Go to **Routing Policies** > **New**.
    2. Configure:
       * **Name**: `Route-via-Retell`
       * **SIP Entity**: `SBCE-Retell-Trunk`.
       * **Retries**: `1`.
    3. Save.

    **4. Configure Dial Patterns (Incoming Call Route)**

    Dial patterns map DIDs arriving from Retell to the correct destination within Aura (e.g., a Communication Manager trunk group or a SIP entity).

    1. Go to **Dial Patterns** > **New**.
    2. Configure:
       * **Pattern**: your DID or DID range (e.g., `+1212555` prefix or full E.164 `+12125551234`).
       * **Min / Max**: set to match the digit length.
       * **SIP Domain**: your internal SIP domain.
       * **Routing Policy**: `Route-via-Retell` (for outbound to Retell) or a policy pointing to Communication Manager (for inbound).
    3. Save and **Commit** the routing configuration.
  </Step>

  <Step title="Configure Communication Manager — Trunk Group and Incoming Route">
    Communication Manager configuration is accessed through **System Manager** > **Elements** > **Communication Manager** > **Launch Element Manager**, or directly via SAT terminal.

    **1. Create a SIP Signaling Group**

    1. In CM Element Manager, go to **Telephony** > **Trunks** > **Signaling Groups** > **Add**.
    2. Configure:
       * **Group Type**: `sip`
       * **Transport Method**: `tcp` (or `tls`)
       * **Near-end Node Name**: the CM node name for your processor interface.
       * **Near-end Listen Port**: `5060`
       * **Far-end Node Name**: the node name for Session Manager (defined under **IP Node Names**).
       * **Far-end Listen Port**: `5060`
       * **Far-end Network Region**: assign to the network region used for Retell traffic.
       * **Direct IP-IP Audio Connections**: `y` (enables media hairpinning bypass where possible).
       * **DTMF over IP**: `rtp-payload` (RFC 2833 — compatible with Retell).
    3. Save.

    **2. Create a Trunk Group**

    1. Go to **Telephony** > **Trunks** > **Trunk Groups** > **Add**.
    2. Configure:
       * **Group Type**: `sip`
       * **Group Name**: `Retell-Trunk`
       * **COR**: assign an appropriate Class of Restriction.
       * **Signaling Group**: the signaling group number from the previous step.
       * **Number of Members**: set to your expected max concurrent calls.
    3. Under the **Trunk Parameters** tab:
       * **Codecs**: ensure PCMU/PCMA is included (CM negotiates via SDP with Session Manager).
       * **Incoming Destination**: leave blank or set to a default VDN/extension.
    4. Save.

    **3. Configure Incoming Call Handling (Incoming Call Route)**

    Map inbound DIDs to extensions, VDNs, or hunt groups in CM.

    1. Go to **Telephony** > **Trunks** > **Trunk Groups** > select your trunk group > **Incoming Call Handling**.
    2. Add entries mapping your DID numbers:
       * **Trunk Group**: your Retell trunk group number.
       * **Incoming Destination**: the VDN, extension, or hunt group to ring.
       * **Delete Digits / Insert**: modify dialed digits if your routing requires digit translation.
    3. Save.

    **4. Configure Outbound Routing (AAR / ARS)**

    To route outbound calls from CM agents through the Retell trunk:

    1. Go to **Routing** > **AAR Analysis** (for internal routing) or **ARS Analysis** (for PSTN routing).
    2. Add a route pattern:
       * **Route Pattern**: assign a route pattern number.
       * **Grp No**: your Retell trunk group number.
       * **FRL**: set the Facility Restriction Level.
       * **Numbering Format**: `public` (E.164).
    3. Update your **Dial Plan** and **ARS Digit Analysis** to steer calls to this route pattern.
    4. Save.
  </Step>

  <Step title="TLS and SRTP with Retell">
    Use TLS and SRTP when end-to-end signaling and media encryption is required between Retell and the Avaya SBCE.

    **How it works:**

    * **TLS** encrypts the SIP signaling between Retell and the SBCE A-side.
    * **SRTP** encrypts the RTP media. Retell requires TLS transport to enable SRTP.
    * The SBCE terminates TLS on the A-side and can re-encrypt or pass media unencrypted on the B-side (toward Session Manager), depending on your internal security policy.

    **Retell SIP URI for TLS:**

    ```
    sip:sip.retellai.com;transport=tls
    ```

    Use this URI when configuring the Server Configuration on SBCE (port `5061`) and when importing the number into Retell.

    **SBCE TLS configuration:**

    1. In the SBCE EMS, go to **TLS Management** > **Certificates**.
    2. Import the Retell Root CA and intermediate CA so the SBCE trusts Retell's certificate during TLS handshake:
       * **Root CA**: Amazon Root CA 1 — download `AmazonRootCA1.pem` from the [Amazon Trust Services repository](https://www.amazontrust.com/repository/).
       * **Intermediate CA**: `C=US, O=Amazon, CN=Amazon RSA 2048 M01` — also available at the [Amazon Trust Services repository](https://www.amazontrust.com/repository/). Install this if the SBCE requires the full chain for validation.
    3. In **Signaling Interface** (`Service-Provider-External`), ensure **TLS Port** `5061` is configured.
    4. In **Server Configuration** (`Service-Provider`), set **Transport** to `TLS` and **Port** to `5061`.
    5. Under **Security Rules** (used in the End Point Policy Group), create or select a rule that enforces:
       * **TLS**: enabled.
       * **SRTP**: enabled.
       * **SRTP Cipher**: `AES_CM_128_HMAC_SHA1_80` (recommended and compatible with Retell).

    **Session Manager TLS (internal leg):**

    If you also want TLS between the SBCE B-side and Session Manager, update the Entity Link to use `TLS` on port `5061` and ensure the Session Manager identity certificate is trusted by the SBCE.

    **Firewall additions for TLS/SRTP:**

    | Protocol | Port       | Purpose                                |
    | -------- | ---------- | -------------------------------------- |
    | TCP      | 5061       | SIP/TLS between Retell and SBCE A-side |
    | UDP      | 1024–65535 | SRTP media (same port range as RTP)    |
  </Step>

  <Step title="Save and Commit Configuration">
    Changes across the Aura stack must be saved and committed before they take effect.

    **SBCE:**

    * Most changes in the SBCE EMS take effect immediately on save, but verify under **Monitoring** > **Server Status** that the SBCE service is active and no alarms are raised.

    **Session Manager / System Manager:**

    1. In System Manager, after saving routing changes (SIP Entities, Entity Links, Dial Patterns, Routing Policies), click **Commit** in the top-right of the Routing module.
    2. Confirm the commit succeeds and Session Manager shows the updated routing in **Elements** > **Session Manager** > **System Status**.

    **Communication Manager:**

    1. If using SAT terminal: type `save translation` to persist changes.
    2. If using CM Element Manager: changes are saved per screen — verify all trunk group and signaling group entries show the expected values.
    3. For busy production systems, schedule a maintenance window before committing trunk group changes.
  </Step>

  <Step title="Import the Number into Retell">
    After the Avaya side is configured, import the phone number into Retell so Retell knows which trunk to use for outbound calls and which agent to assign for inbound.

    1. In the Retell dashboard, go to **Phone Numbers** > **Import Number**.
    2. Fill in:
       * **Phone Number**: E.164 format (e.g., `+12137771234`).
       * **Termination SIP URI**: The SBCE A-side IP or FQDN with port (e.g., `<sbce-public-ip>:5060` or `<sbce-fqdn>:5060`). For TLS: `<sbce-fqdn>:5061` and ensure you use `sip:...;transport=tls`.
       * **SIP Username / Password**: Only required if you enabled inbound digest authentication on the SBCE End Point Policy Group.
    3. Save the number and assign a Retell agent to it.

    You can also import numbers programmatically via the [Import Number API](/api-references/import-phone-number).

    Once imported, the number works for both inbound and outbound calls — see [Make Outbound Calls](/deploy/outbound-call) and [Receive Inbound Calls](/deploy/inbound-call).
  </Step>

  <Step title="Test the SIP Trunk">
    **Inbound test (external call → Avaya DID → Retell agent):**

    1. Call the DID from an external phone.
    2. Verify the call traverses: PSTN → CM → SM → SBCE → Retell.
    3. Confirm the call appears in Retell's **Calls** dashboard and the correct agent handles it.
    4. Verify bidirectional audio and clean call termination.

    **Outbound test (Retell → SBCE → CM → PSTN):**

    1. Place an outbound call via the Retell dashboard or [Create Phone Call API](/api-references/create-phone-call) using the imported number.
    2. Confirm the receiving party sees the correct caller ID (E.164 format).
    3. Verify audio quality in both directions.

    **SIP OPTIONS ping test:**
    If you enabled heartbeat/OPTIONS on the SBCE Server Configuration, check **SBCE EMS** > **Monitoring** > **Server Status** to confirm the trunk shows as **Active** based on OPTIONS responses from `sip.retellai.com`.
  </Step>

  <Step title="Debug Call Issues">
    **1. SBCE Trace (SIP and Media)**

    The SBCE provides packet-level and SIP-level traces via the EMS.

    * Go to **Monitoring** > **Incidents** for active alarms and recent error events.
    * Go to **Monitoring** > **Tracing** > **Packet Capture** to capture SIP and RTP packets on the A-side interface during a test call.
    * Go to **Monitoring** > **Tracing** > **Call Trace** (if available on your SBCE release) to see SIP message flow per call.

    Look for:

    * `403 Forbidden` → Retell IP not in SBCE's trusted source list. Check **End-Point Policy Group** and **Server Flow** source matching.
    * `480 Temporarily Unavailable` / `503` → SBCE cannot reach `sip.retellai.com`. Verify DNS resolution and firewall on port 5060/5061.
    * `488 Not Acceptable Here` → Codec mismatch in SDP. Ensure PCMU or PCMA is in the SBCE Media Rule.
    * No audio / one-way audio → RTP being blocked. Check SBCE media port range firewall rules and verify SDP `c=` lines in the trace show the correct SBCE A-side IP (topology hiding should replace internal IPs).

    **2. Session Manager Logs**

    In System Manager, go to **Elements** > **Session Manager** > **System Status** > **Call Routing Test** to simulate a call and verify dial pattern matching.

    Check SM logs under **Elements** > **Session Manager** > **System Logs** for SIP routing rejections or entity link failures.

    **3. Communication Manager**

    On CM, use the SAT commands:

    * `list trace tac <tac>` — trace calls on a specific trunk access code.
    * `status trunk <group>/<member>` — check the state of individual trunk members.
    * `list measurements trunk-group <group> last-hour` — view call volume and failure stats per trunk group.

    **4. Common Issues**

    | Symptom                    | Likely Cause                            | Fix                                                                 |
    | -------------------------- | --------------------------------------- | ------------------------------------------------------------------- |
    | 403 on inbound from Retell | SBCE rejecting Retell IP                | Add Retell CIDRs to SBCE trusted source / Server Flow               |
    | 503 to Retell              | DNS failure or firewall blocking egress | Check DNS for `sip.retellai.com`, open port 5060 outbound           |
    | No audio                   | RTP port range blocked                  | Open UDP media ports on perimeter firewall and SBCE                 |
    | One-way audio              | NAT / topology hiding issue             | Verify SBCE A-side IP is in SDP `c=`; check topology hiding profile |
    | 488 codec mismatch         | No shared codec in SDP                  | Add PCMU/PCMA to SBCE Media Rule                                    |
    | TLS handshake failure      | Missing CA cert on SBCE                 | Import Amazon Root CA 1 and intermediate into SBCE TLS store        |
    | Trunk shows Down           | Options ping failing                    | Check firewall allows SIP OPTIONS from SBCE to Retell IPs           |
    | Calls drop at \~30s        | SIP re-INVITE blocked mid-call          | Allow mid-call SIP signaling through firewall                       |

    <Note>
      If you cannot resolve the issue, collect the SBCE packet capture, the SM call routing test result, the CM trace, and the Retell Call ID from the Retell dashboard, and send them to us on the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com).
    </Note>
  </Step>
</Steps>


# Retell Website Widget
Source: https://docs.retellai.com/deploy/chat-widget

Learn how to embed the Retell website widget on your site

## Overview

The Retell embeddable website widget is a production-ready, customizable, and secure widget for websites, powered by the Retell API. The widget is embeddable via a single `<script>` tag and uses the Retell public key system, allowing direct API calls from the frontend—no backend proxy required.

The widget supports two modes:

* **Chat & Voice Widget**: Text-based conversations and real-time voice calls, powered by chat and/or voice agents
* **Callback Widget**: Phone-based conversations using a voice agent

<Frame>
  <img alt="Retell Website Widget" />
</Frame>

## Prerequisites

Before embedding either widget, you'll need:

1. **Create an Agent**:

* For **chat widget**: Create a chat agent using the [Create Chat Agent](/build/create-chat-agent) guide. Optionally, create a voice agent to enable voice calls within the chat widget.
* For **callback widget**: Create a voice agent to handle phone conversations

2. **Get Your Credentials**:

* Your [Retell Public Key](/accounts/public-keys)
* Your Retell agent ID (chat agent for text chat, voice agent for voice calls or callback)
* For callback widget: Your Retell phone number

## Chat Widget

The chat widget provides text-based conversations through a chat interface. When a voice agent is also configured, users can make real-time voice calls directly within the widget.

### Setup

Add the following script tag to your HTML, within the `<head>` tag:

```html theme={null}
<script
    id="retell-widget"
    src="https://dashboard.retellai.com/retell-widget-v2.js"
    type="module"
    data-public-key="YOUR_RETELL_PUBLIC_KEY"
    data-agent-id="YOUR_CHAT_AGENT_ID"
    data-voice-public-key="YOUR_VOICE_PUBLIC_KEY"
    data-voice-agent-id="YOUR_VOICE_AGENT_ID"
    data-agent-version="YOUR_AGENT_VERSION"
    data-title="YOUR_CUSTOM_TITLE"
    data-logo-url="YOUR_LOGO_URL"
    data-color="YOUR_CUSTOM_COLOR"
    data-theme-color="YOUR_THEME_COLOR"
    data-component-color="YOUR_COMPONENT_COLOR"
    data-fab-text="YOUR_FAB_TEXT"
    data-bot-name="YOUR_BOT_NAME"
    data-popup-message="YOUR_POPUP_MESSAGE"
    data-show-ai-popup="true"
    data-show-ai-popup-time="5"
    data-auto-open="false"
    data-dynamic='{"key": "value"}'
    data-white-label="YOUR_WHITE_LABEL_TOKEN"
    data-recaptcha-key="YOUR_GOOGLE_RECAPTCHA_SITE_KEY"
></script>
```

### Chat Widget Attributes

**Required (at least one):**

* `data-public-key` - Your Retell public key (used for chat API)
* `data-voice-public-key` - Separate public key for voice/web call API. At least one of `data-public-key` or `data-voice-public-key` is required.

**Optional — Agent Configuration:**

* `data-agent-id` - Your chat agent ID (enables text chat)
* `data-voice-agent-id` - Your voice agent ID (enables real-time voice calls). When both `data-agent-id` and `data-voice-agent-id` are set, the widget displays a chooser screen letting users pick between voice and chat.
* `data-agent-version` - Agent version (if unset, uses latest version)
* `data-dynamic` - JSON string with dynamic variables for the chat agent (e.g., `'{"company": "Acme"}'`)

**Optional — Appearance:**

* `data-title` - Custom chat window title (default: `"Chat"`)
* `data-logo-url` - URL of your logo image
* `data-color` - Hex color code for widget theme (e.g., `"#FFA07A"`). Acts as a shorthand that sets both `data-theme-color` and `data-component-color`.
* `data-theme-color` - Hex color for the widget theme/background (default: `"#071a3e"`). Overrides `data-color` for the theme.
* `data-component-color` - Hex color for accent elements like buttons and links (default: `"#3E6AEF"`). Overrides `data-color` for components.
* `data-fab-text` - Text displayed on the floating action button (default: `"Need support?"`)

**Optional — Behavior:**

* `data-bot-name` - Bot name for popup messages (default: `"AI Assistant"`)
* `data-popup-message` - Popup message before users open chat
* `data-show-ai-popup` - Set to `"true"` to enable popup messages, `"false"` to disable (default: `"true"`)
* `data-show-ai-popup-time` - Seconds to delay before showing popup (default: `5`)
* `data-auto-open` - Set to `"true"` to auto-open chat widget on page load (default: `"false"`)

**Optional — Security & Branding:**

* `data-recaptcha-key` - Google reCAPTCHA v3 site key for bot protection (**Note: Only reCAPTCHA v3 is supported**)
* `data-white-label` - White-label token to hide "Powered by Retell" branding. Contact Retell to obtain your token.

### Color Customization

The chat widget supports flexible color customization through a fallback chain:

| Attribute              | CSS Variable        | Default   | Description                                         |
| ---------------------- | ------------------- | --------- | --------------------------------------------------- |
| `data-theme-color`     | `--color-theme`     | `#071a3e` | Widget theme/background color                       |
| `data-component-color` | `--color-component` | `#3E6AEF` | Accent color for buttons, links, etc.               |
| `data-color`           | —                   | —         | Shorthand that sets both theme and component colors |

**Fallback logic:**

* `data-theme-color` falls back to `data-color` if not set
* `data-component-color` falls back to `data-color` if not set

This means you can use `data-color` alone for a simple single-color theme, or combine `data-theme-color` and `data-component-color` for fine-grained control.

### Voice + Chat Hybrid Mode

When both `data-agent-id` and `data-voice-agent-id` are provided, the widget enters **hybrid mode**:

1. Users see a **chooser screen** with "Voice Assistant" and "Chat Assistant" options
2. A **tab bar** at the bottom allows switching between voice and chat at any time
3. Voice calls use WebRTC for real-time audio with a built-in audio visualizer
4. Chat sessions are persisted locally and can be resumed

If only `data-agent-id` is set, the widget goes directly to the chat interface.
If only `data-voice-agent-id` is set, the widget goes directly to the voice call interface.

### reCAPTCHA Protection

The chat widget supports Google reCAPTCHA v3 for bot protection. **Important: Only reCAPTCHA v3 is supported.**

To enable reCAPTCHA:

1. Include the Google reCAPTCHA v3 script in your HTML `<head>` tag:

```html theme={null}
<script src="https://www.google.com/recaptcha/api.js?render=YOUR_GOOGLE_RECAPTCHA_SITE_KEY"></script>
```

2. Add the `data-recaptcha-key` attribute to your widget script with your reCAPTCHA v3 site key
3. Enable reCAPTCHA protection for your public key in the [Retell Public Keys settings](/accounts/public-keys)

### How Chat Widget Works

1. User clicks the chat widget button (displays the FAB button with customizable text)
2. If voice agent is configured, a chooser screen appears; otherwise, chat opens directly
3. **Text chat**: User types messages and receives responses from the chat agent. Chat sessions are automatically persisted in the browser's localStorage and can be resumed later.
4. **Voice calls**: User clicks "Voice Assistant" to start a real-time WebRTC voice call with the agent. A built-in audio visualizer displays the conversation in real time.
5. If reCAPTCHA is enabled, bot protection is automatically applied to new chat sessions and voice calls

### Testing Chat Widget

After adding the widget to your website:

1. Load your website
2. Click the floating button (bottom right)
3. If both agents are configured, choose between voice or chat mode
4. Start a conversation with your agent

### Example: Chat Widget (Text Chat Only)

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Retell Chat Widget Example</title>
    <script src="https://www.google.com/recaptcha/api.js?render=YOUR_GOOGLE_RECAPTCHA_SITE_KEY"></script>
    <script
      id="retell-widget"
      src="https://dashboard.retellai.com/retell-widget-v2.js"
      data-public-key="key_xxxxxxxxxxxxxxxxxxxxx"
      data-agent-id="agent_xxxxxxxxxxxxxxxxxxx"
      data-agent-version="0"
      data-title="Chat with us!"
      data-recaptcha-key="YOUR_GOOGLE_RECAPTCHA_SITE_KEY"
    ></script>
  </head>
  <body></body>
</html>
```

### Example: Chat Widget (Voice + Chat Hybrid)

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Retell Voice + Chat Widget Example</title>
    <script src="https://www.google.com/recaptcha/api.js?render=YOUR_GOOGLE_RECAPTCHA_SITE_KEY"></script>
    <script
      id="retell-widget"
      src="https://dashboard.retellai.com/retell-widget-v2.js"
      data-public-key="key_xxxxxxxxxxxxxxxxxxxxx"
      data-voice-public-key="key_xxxxxxxxxxxxxxxxxxxxx"
      data-agent-id="agent_chat_xxxxxxxxxxxxxxx"
      data-voice-agent-id="agent_voice_xxxxxxxxxxx"
      data-title="How can we help?"
      data-color="#FFA07A"
      data-recaptcha-key="YOUR_GOOGLE_RECAPTCHA_SITE_KEY"
    ></script>
  </head>
  <body></body>
</html>
```

## Callback Widget

The callback widget collects user information and initiates a phone call instead of a chat session. This mode requires a voice agent to handle the phone conversation.

<Frame>
  <img alt="Retell Callback Widget" />
</Frame>

### Setup

Add the following script tag to your HTML, within the `<head>` tag:

```html theme={null}
<script
  id="retell-widget"
  src="https://dashboard.retellai.com/retell-widget-v2.js"
  type="module"
  data-public-key="YOUR_RETELL_PUBLIC_KEY"
  data-agent-id="YOUR_VOICE_AGENT_ID"
  data-widget="callback"
  data-phone-number="YOUR_RETELL_PHONE_NUMBER"
  data-title="Request a Call"
  data-countries="US,CA,GB"
  data-tc="https://yoursite.com/terms"
  data-color="#FFA07A"
  data-recaptcha-key="YOUR_GOOGLE_RECAPTCHA_SITE_KEY"
  data-fab-text="Get a call from us"
></script>
```

### Callback Widget Attributes

**Required:**

* `data-public-key` - Your Retell public key
* `data-agent-id` - Your voice agent ID (not chat agent)
* `data-widget="callback"` - Enables callback mode
* `data-phone-number` - Your Retell phone number that will make the outbound call

**Optional:**

* `data-title` - Custom widget title
* `data-color` - Hex color code for widget theme
* `data-countries` - Comma-separated country codes for country selector (e.g., "US,CA,GB")
* `data-tc` - URL to your terms and conditions page
* `data-recaptcha-key` - Google reCAPTCHA v3 site key for bot protection

### How Callback Widget Works

**Note:** The callback widget supports the same reCAPTCHA v3 protection as the chat widget. To enable it, follow the instructions in the [reCAPTCHA Protection](#recaptcha-protection) section above.

1. User clicks the callback widget button (displays a phone icon)
2. A form appears collecting:

* First name (required)
* Last name (required)
* Phone number (required)
* Privacy policy agreement checkbox (required)

3. User submits the form
4. If reCAPTCHA is enabled, the form submission is validated
5. The widget creates a phone call using the Retell API
6. User receives a call from your specified phone number
7. The conversation is handled by your configured voice agent

### Testing Callback Widget

After adding the widget to your website:

1. Load your website
2. Click the floating button (bottom right, phone icon)
3. Fill out the contact form
4. Submit and wait for the phone call

### Example: Callback Widget

```html theme={null}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Retell Callback Widget Example</title>
    <script src="https://www.google.com/recaptcha/api.js?render=YOUR_GOOGLE_RECAPTCHA_SITE_KEY"></script>
    <script
      id="retell-widget"
      src="https://dashboard.retellai.com/retell-widget-v2.js"
      data-public-key="key_xxxxxxxxxxxxxxxxxxxxx"
      data-agent-id="agent_xxxxxxxxxxxxxxxxxxx"
      data-widget="callback"
      data-phone-number="+15551234567"
      data-title="Request a Call"
      data-countries="US,CA,GB"
      data-tc="https://example.com/terms"
      data-color="#FFA07A"
      data-recaptcha-key="YOUR_GOOGLE_RECAPTCHA_SITE_KEY"
      data-fab-text="Get a call from us"
    ></script>
  </head>
  <body></body>
</html>
```

## Widget Behavior Summary

* **Chat Widget (text only)**: Shows FAB button, opens chat interface for text conversations with persisted chat history
* **Chat Widget (voice + chat)**: Shows FAB button, displays chooser screen for voice calls or text chat with tab switching
* **Callback Widget**: Shows phone icon, opens form to collect contact info and initiates phone call


# Understand concurrency & limits
Source: https://docs.retellai.com/deploy/concurrency

Understand the constraints and limitations of the agents.

We have enforced some constraints and limitations to ensure the smooth operation of your agents, and prevent
any misuse of the service. Note that these constraints can be adjusted based on your operational needs,
on a case-by-case basis.

## Concurrency

**Concurrency** refers to the number of simultaneous active voice calls that can be handled by your system at any given moment. For example, if 15 users are engaged in voice calls with your agents at the same time, that counts as 15 concurrent calls.

As part of our service, Pay-As-You-Go users are allocated a quota of **20 concurrent calls**.
Should your operational needs require additional concurrency, you can go to "Billing" page to upgrade your plan.

<Frame>
  <img alt="Billing page with concurrency limit settings" />
</Frame>

You can check your current number of concurrent calls in the dashboard.

* **Handling Multiple Calls per Agent**:
  You don't need to create multiple agents to manage multiple calls concurrently.
  Each agent within your plan is capable of handling an unlimited number of calls,
  provided that the total concurrency remains within your designated quota.
  This means you can efficiently manage your workload without unnecessary agent duplication.

## Reserved Inbound Concurrency

Reserved inbound concurrency protects inbound calls from being crowded out by outbound traffic.
When `reserved_inbound_concurrency` is configured, outbound calls can use at most your concurrency
limit minus the reserved amount. Inbound calls can still use the full concurrency limit when capacity
is available.

For example, if your concurrency limit is **100** and reserved inbound concurrency is **20**:

* Outbound calls can use up to **80** slots.
* Inbound calls can use the reserved **20** slots, plus any other available slots up to the full **100**.

You can check the configured value with the [Get Concurrency API](/api-references/get-concurrency).
Reserved inbound concurrency must be lower than your standard concurrency limit.

## Inbound Queue and Fallback

When inbound call traffic reaches your concurrency limit, Retell briefly keeps new inbound calls
waiting for an available slot. If a slot opens, the inbound call proceeds.

If no slot opens after about **40 seconds**, Retell handles the call as follows:

1. If the phone number has a `fallback_number` configured, Retell transfers the caller to that number.
2. If there is no fallback number, or the fallback transfer fails, the call ends with
   `concurrency_limit_reached`.
3. If the fallback transfer succeeds, the Retell call record ends with `no_concurrency_fallback`.

## Concurrency Burst

**Concurrency Burst** allows you to temporarily exceed your standard concurrency limit during peak demand periods. When enabled, calls that would normally be rejected due to hitting your concurrency limit will instead be allowed to proceed with an additional surcharge.

### How It Works

When concurrency burst is enabled:

1. **Normal calls**: Calls within your standard concurrency limit proceed as usual with no additional charges
2. **Burst calls**: Calls that exceed your normal limit (but stay within the burst limit) will proceed with an additional **\$0.10/min** surcharge applied to the entire call duration

### Burst Limit Calculation

Your burst limit is calculated as the **lower** of:

* **3× your concurrency limit**, OR
* **Your concurrency limit + 300**

For example:

* If your limit is **50**, burst allows up to **150** concurrent calls (3 × 50 = 150)
* If your limit is **200**, burst allows up to **500** concurrent calls (200 + 300 = 500, which is less than 3 × 200 = 600)

### Enabling Concurrency Burst

You can enable or disable concurrency burst from the **Settings > Limits** page in your dashboard.

<Frame>
  <img alt="Concurrency Burst Settings" />
</Frame>

### Pricing

| Call Type                      | Additional Cost                             |
| ------------------------------ | ------------------------------------------- |
| Normal (within standard limit) | No additional charge                        |
| Burst (above standard limit)   | **\$0.10/min** for the entire call duration |

<Note>
  The burst surcharge applies to the **entire duration** of any call that started while in burst mode, not just the portion of time spent above the normal limit.
</Note>

### Use Cases

Concurrency burst is ideal for:

* **Unpredictable traffic spikes**: Handle sudden increases in call volume without rejected calls
* **Campaign launches**: Support higher-than-normal call volumes during marketing campaigns
* **Seasonal peaks**: Manage increased demand during busy periods without permanently upgrading your concurrency limit

<Warning>
  While concurrency burst provides flexibility, consistent high usage above your normal limit may indicate a need to increase your base concurrency allocation for cost efficiency.
</Warning>

## Max Call Duration

The maximum duration of a call is **1 hour** by default, and the call will end automatically after 1 hour. You can increase this up to **2 hours** in your agent settings.
Should your operational needs require longer calls, please reach out to our team at
[support@retellai.com](mailto:support@retellai.com) to discuss options.

## Max Prompt Token Length

The maximum length of prompt when using Retell LLM framework is **32768** by default, and longer prompt will be rejected
when creating or updating the LLM. Note that prompts over 3500 tokens will be charged extra, read more at [Billing Exceptions](/accounts/billing-exceptions).
Should your operational needs require longer context, please reach out to our team at
[support@retellai.com](mailto:support@retellai.com) to discuss options.


# Create Chat Completion
Source: https://docs.retellai.com/deploy/create-chat-completion

A step-by-step guide to implementing chat functionality with Retell

This guide explains how to implement chat functionality using Retell's Chat API. You'll learn how to start a chat session, generate responses, and end the session.

<Steps>
  <Step title="Create a Chat Agent">
    Before starting a chat session, you need a chat agent to handle the conversation.

    For detailed instructions on creating a chat agent, refer to the [Create Chat Agent](/build/create-chat-agent) guide.
  </Step>

  <Step title="Create a Chat Session">
    To start a chat session, use the `create-chat` API endpoint.

    The API will return a `chat_id` that you'll need for subsequent requests.

    For detailed API information, refer to the [Create Chat API Reference](/api-references/create-chat).
  </Step>

  <Step title="Create a Chat Completion">
    To generate a response from the chat agent, use the `create-chat-completion` API endpoint.

    The API will return the agent's response in the `messages` array. All conversation history is automatically stored in Retell's database, so you don't need to manage conversation context yourself.

    For detailed API information, refer to the [Create Chat Completion API Reference](/api-references/create-chat-completion).
  </Step>

  <Step title="Retrieve Chat Details">
    You can retrieve details about a chat session using the `get-chat` API endpoint.

    You can also list chat sessions using the `POST /v3/list-chats` endpoint.

    For detailed API information, refer to the [Get Chat API Reference](/api-references/get-chat) and [List Chats API Reference](/api-references/list-chats).
  </Step>

  <Step title="End Chat Session">
    When the conversation is complete, end the chat session using the `end-chat` API endpoint.

    If Auto-Close Inactive Chats is enabled, chat will automatically end when the timeout is triggered, or you can end them anytime with the `end-chat` API.

    For detailed API information, refer to the [End Chat API Reference](/api-references/end-chat).
  </Step>
</Steps>

## SMS Integration

Retell also supports Twilio SMS integration, allowing you to deploy your chat agents to receive and respond to text messages. To enable SMS functionality for your chat agents, refer to the [Enable SMS](/deploy/enable-sms) guide.

Once you complete the SMS integration setup, you'll have access to:

* **Make an outbound SMS** button to start a new SMS session
* Inbound SMS agent configuration
* Outbound SMS agent configuration
* Inbound webhook setup for receiving SMS messages

<Note>
  **SMS** conversations with your chat agent on a phone number can include **multimedia** (for example MMS). **Text chat** via the `create-chat-completion` API does not support images or other multimedia.
</Note>


# Custom Telephony Overview
Source: https://docs.retellai.com/deploy/custom-telephony

A step by step guide to integrate custom telephony providers

## Overview

In this guide, we will show how to integrate Retell agents with your telephony providers
and use your numbers. Please note that this is independent of the agent type you are using.

We will provide two ways to integrate with your telephony provider:

1. **Elastic SIP trunking**: This is the **recommended** way to integrate with
   your telephony provider that supports elastic SIP trunking. You will need to set up
   a SIP trunking and configure your number to point to it, and then import that number
   to Retell.
2. **Dial to SIP URI**: If your telephony provider does not support elastic SIP trunking,
   or you have more complicated telephony setup that cannot use elastic SIP trunking,
   you can dial the call to a specific SIP uri.

<Note>
  * Retell SIP server uri: `sip:sip.retellai.com`
  * IP block for traffic: `18.98.16.120/30` (All regions), `143.223.88.0/21` (certain United States traffic), `161.115.160.0/19` (certain United States traffic)

  You can use the IP block to whitelist the traffic to Retell's SIP server. It's commonly needed in a bunch of telephony providers.
</Note>

Transport method supported:

* TCP (Recommended)
* UDP
* TLS
* mTLS ([Learn more](#mutual-tls-mtls))

For using the different transport for inbound calls, you can postpend the transport method to the sip server url:

* For TCP, the sip server url needs to be `sip:sip.retellai.com;transport=tcp`
* For UDP, the sip server url needs to be `sip:sip.retellai.com;transport=udp`
* For TLS, the sip server url needs to be `sip:sip.retellai.com;transport=tls`

Media encryption supported:

* SRTP (Transport should be set to TLS to use SRTP)

Audio Codecs supported:

* PCMU
* PCMA
* G.722(HD)

## Method 1: Elastic SIP trunking (Recommended)

Elastic SIP Trunking is a service offered by cloud communications platforms that enables
organizations to connect their existing PBX (Private Branch Exchange) or VoIP (Voice over IP)
infrastructure to the Public Switched Telephone Network (PSTN) over the internet using the
SIP (Session Initiation Protocol).

In this context, the elastic SIP trunking is used to connect Retell's VoIP with
PSTN so that your agents can make and receive calls. When using this method, all the telephony functionalities that are
supported by Retell numbers will also be supported here, assuming that your telephony provider supports it.

SIP trunking is a popular service offered by many telephony providers, so most likely
your telephony provider would be able to support this.

Here're detailed guides for some telephony providers:

* [Twilio](/deploy/twilio)
* [Telnyx](/deploy/telnyx)
* [Vonage](/deploy/vonage)

Other telephony providers that support SIP trunks are also supported, feel free to use these guides as a reference.

### FAQ

<AccordionGroup>
  <Accordion title="Will it throw errors if the details or configuration is incorrect?">
    No, Retell will not be able to know if the setup you provide works or not until a call is made.
  </Accordion>

  <Accordion title="My inbound call is not connecting, what should I do?">
    Please check your origination setting in your SIP trunking provider. Also check the logs in your telephony provider,
    and perhaps open a ticket with them.
  </Accordion>

  <Accordion title="My outbound call is not connecting, what should I do?">
    Please check your termination setting in your SIP trunking provider, and make sure you provide the right termination url to Retell.
    Also check the logs in your telephony provider, and perhaps open a ticket with them.
  </Accordion>

  <Accordion title="Will I be able to transfer call using SIP trunking?">
    Yes you can use the transfer call feature with SIP trunking. Please note that if you intend to use SIP REFER (cold transfer
    with the transferee's number), you will need to configure that in your SIP trunking provider to allow SIP REFER and PSTN transfer,
    with the transferee's number showing as caller id.
  </Accordion>

  <Accordion title="Will I be able to press digit using SIP trunking?">
    Yes, you can.
  </Accordion>

  <Accordion title="Can I view and manage the numbers I import using SIP trunking?">
    Yes, you can.
  </Accordion>

  <Accordion title="I need to change the configuration of the imported number, how can I do that?">
    Right now you'd need to delete and re-import the number.
  </Accordion>
</AccordionGroup>

## Method 2: Dial to SIP URI

If your telephony provider does not support elastic SIP trunking, or you have more complicated
telephony setup that cannot use elastic SIP trunking, you can use this method.

When using this method, Retell does not directly make or receive calls, but instead
relies on your system to dial the call to the respective SIP URI. This would require you to
have some codes to handle integration with your telephony provider. All traffic looks like
inbound to Retell in this case, so it's up to you to specify the call direction.

<Warning>When using this method, you will not be able to utilize Retell's transfer call feature, as we do not
have access and control over the telephony provider and number, and cannot initiate transfer for you. You can however implement your own transfer logic and use a custom function to trigger a call transfer.</Warning>

Here we assume you already have your call handling setup.
For Retell to know what agent to use to handle the call, and for you to
**obtain SIP URI to use** for this call, you would call the
[Register Phone Call API](/api-references/register-phone-call).
You will get a `call_id` back from this API, and you would use it to piece
together the SIP URI.

<Note>SIP URI: `sip:{call_id}@sip.retellai.com`</Note>

<Warning>
  You must dial the call to the SIP URI within **5 minutes** of calling Register Phone Call. If the call is not connected within that window, it disconnects with `registered_call_timeout`. See [Debug call disconnection](/reliability/debug-call-disconnect) for disconnection reasons.
</Warning>

### Example Code

Here's an overly simplified example code to handle the inbound call
webhook from Twilio and dialing the call to the SIP URI.

```Typescript Node theme={null}
const client = new Retell({
  apiKey: 'YOUR_RETELL_API_KEY',
});

server.app.post(
  "/voice-webhook",
  async (req: Request, res: Response) => {
    // Register the phone call to get call id
    const phoneCallResponse = await client.call.registerPhoneCall({
      agent_id: 'oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD',
      from_number: "+12137771234", // optional
      to_number: "+12137771235", // optional
      direction: "inbound", // optional
    });

    // Start phone call websocket
    const voiceResponse = new VoiceResponse();
    const dial = voiceResponse.dial();
    dial.sip(
      `sip:${phoneCallResponse.call_id}@sip.retellai.com`,
    );
    res.set("Content-Type", "text/xml");
    res.send(voiceResponse.toString());
  },
);

```

### FAQ

<AccordionGroup>
  <Accordion title="How to transfer call/end call using dial to SIP method?">
    You will need to handle the transfer call/end call logic yourself, meaning that you will need to write a custom function which internally
    interacts with your telephony provider to transfer the call/end the call.
  </Accordion>

  <Accordion title="Will I be able to press digit using dial to SIP method?">
    Yes.
  </Accordion>

  <Accordion title="Two entries created for a single dial?">
    Check your code that interacts with telephony provider. Some provider like Twilio can call the webhook multiple times for a single call.
    In those cases, you will need to dedupe the call.
  </Accordion>

  <Accordion title="Can I use telephony provider's other features like AMD detection using this method?">
    Yes, using this method basically gives you full control over telephony functionalities, so you should be able to use telephony provider's
    other features.
  </Accordion>
</AccordionGroup>

## Security Center

Retell is built on enterprise-grade security to protect your voice communications. We recommend using **TLS 1.2 or higher** to secure all SIP signaling channels between your infrastructure and Retell's SIP servers.

To establish a secure TLS connection with Retell's SIP server, you may need to add Retell's server-side root CA to your trust store. You can download it [here](https://www.amazontrust.com/repository/G2-RootCA1.pem).

### Mutual TLS (mTLS)

Mutual TLS (mTLS) is an extension of the standard TLS protocol that provides two-way authentication between a client and a server. Unlike standard TLS — where only the server presents a certificate to prove its identity to the client — mTLS requires **both sides** to present and verify certificates. This ensures that only trusted, authenticated parties can establish a connection, significantly reducing the risk of man-in-the-middle attacks and unauthorized access.

In a typical TLS handshake:

1. The server presents its certificate to the client.
2. The client verifies the server's certificate and the connection is established.

With mTLS, an additional step is added:

1. The server presents its certificate to the client.
2. The **client also presents its certificate** to the server.
3. Both parties verify each other's certificates before the connection is established.

This mutual verification makes mTLS particularly valuable for SIP-based voice infrastructure, where securing signaling and media traffic between trusted systems is critical.

**Retell supports Mutual TLS (mTLS)** for SIP connections, enabling enterprise-grade security for your telephony integrations. If you require mTLS for your setup, please reach out to us via the [Customer Support Portal](https://support.retellai.com/) or at [support@retellai.com](mailto:support@retellai.com) to get it configured for your account.

Retell uses a client certificate issued by AWS Private Certificate Authority (PCA). To validate Retell's TLS client certificate, you **must** add the [root certificate](https://retell-trust-store.s3.us-west-2.amazonaws.com/pca/client-root-ca.pem) to your SIP server's trusted certificate store — without this, your server will reject incoming connections from Retell.

## Video Tutorials

### Elastic SIP Trunking

<div>
  Twilio
</div>

<div>
  <iframe title="Twilio SIP Trunking Integration with Retell" />
</div>

<div>
  Telnyx
</div>

<div>
  <iframe title="Vonage SIP Trunking Integration with Retell" />
</div>

<div>
  Vonage
</div>

<div>
  <iframe title="Vonage SIP Trunking Integration with Retell" />
</div>

### Dial to SIP URI

<div>
  <iframe title="Custom Telephony Integration Demo" />
</div>

## Telephony Partners

In certain scenarios, you might need to manipulate the SIP call flow, or have some custom needs that are not directly supported by Retell, you can check out our telephony partners to see if they can help you.

* [Jambonz](https://www.retellai.com/app-partner/jambonz): Jambonz is a SIP server that supports static IP address and can be used to connect to Retell's SIP server to manipulate the SIP call flow. Dedicated slack support channel is available for Retell users.
* [Cloudonix](https://www.retellai.com/app-partner/cloudonix): Cloudonix is a CPaaS that can be connected to Retell's SIP server to manipulate the SIP call flow.


# Send & receive SMS
Source: https://docs.retellai.com/deploy/enable-sms

A step by step guide to enable SMS capabilities including sending, receiving, and two way conversations

Communication is not bound to voice only. SMS is a common way to communicate with customers. This guide will show you how to enable SMS with Retell Twilio numbers or bring your own Twilio number.

<Warning>SMS capabilities are available for Retell Twilio numbers and custom telephony numbers that have passed A2P applications. Telnyx is not supported yet. For other custom telephony providers, please check your own telephony provider's documentation on how to enable SMS.</Warning>
<Warning>Current SMS capabilities are limited to standard US numbers only. Tollfree numbers are not supported.</Warning>

## Enable SMS capabilities

This step is a prerequisite for sending SMS from your own number during calls and setting up two way SMS conversations. Receiving SMS during calls works out of the box for Retell Twilio numbers without this step.

<Tip>
  If you only need to send SMS during calls and want to skip the A2P application, you can choose to send from an **SMS-approved Retell number** instead. See [Send SMS during call](#send-sms-during-call) for details.
</Tip>

### Option 1: Enable SMS for Retell Twilio Numbers

To enable SMS, it will go through the following application and approval steps:

* Get approved for a business profile (free)
* Get approved for the brand based on business profile (\$4 one time application fee for low-volume, \$45 one time application fee for standard)
* Get approved for a SMS campaign (\$15 one time application fee)

<img />

It can take around 2-3 weeks for the entire application, sometimes longer, as it's a manual review process on the telephony provider side. We will notify you via email when the application is approved or rejected with the reason. If your application is stuck in pending review for over a month, please reach out to support and we will help escalate.

#### Detailed steps

<Steps>
  <Step title="Get approved for a business profile">
    You can reuse an existing business profile or create a new one here. Follow the instructions at [Business Profile](/build/telephony/business-profile) to get approved for a business profile.
  </Step>

  <Step title="Select a brand type and get approved for the brand">
    <Warning>Only one brand can be created per business profile and it cannot be changed once created. If you need to change the brand type, you have to create a new business profile.</Warning>

    Here you get to select two types of brands:

    * Low-volume:
      * \$4 one time application fee
      * send fewer than 6,000 message segments per day to the US (2,000 message segments per day to T-Mobile)
    * Standard:
      * \$45 one time application fee
      * SMS limit may fall between 6,000 and 400,000 message segments per day to the US (2,000 - 200,000 per day to T-Mobile)

    Depending on your company's type, you might be asked to fill out additional information.
  </Step>

  <Step title="Get approved for a SMS campaign">
    <img />

    Here you will fill out the use case, and sample messages you intend to send. Please note that there's very strict rules on SMS, and if your actual traffic doesn't match the sample messages, your number / telephony subaccount might be suspended. Therefore, please be honest and provide answers that match your intended use case. If you ever need to send different SMS messages, you can create a new campaign (check FAQ for more details).
  </Step>
</Steps>

#### Rejected application FAQ

<AccordionGroup>
  <Accordion title="What are some of the common reasons for application rejection?">
    There are a few common reasons for application rejection:

    * the campaign application did not provide detailed information on the use case and sample messages.
    * Opt in workflow was not explained clearly.
    * Business profile or brand was not approved, due to missing or incorrect business information.

    Feel free to read more at [Twilio's A2P 10DLC documentation](https://help.twilio.com/articles/15778026827291-Why-Was-My-A2P-10DLC-Campaign-Registration-Rejected-).
  </Accordion>

  <Accordion title="If my application is rejected, what should I do?">
    Please check the rejection reason and update your application accordingly. If you are rejected at a later stage, you might be able to reuse the previous steps. For example, if your business profile and brand are approved, but the SMS campaign is rejected, you can reuse the business profile and brand approval, and create a new SMS campaign application.
  </Accordion>

  <Accordion title="If my application is rejected, will I get a refund?">
    No, you will not get a refund, as the charge is for the telephony provider's manual review process, and that will be charged regardless of the application outcome.
  </Accordion>

  <Accordion title="How to create a new SMS campaign if I want to change my use case for the number?">
    You can delete the SMS capability on the number (this will not delete your approved business profile and brand, and campaign, those can still be reused), and create a new SMS application with a new campaign while reusing the business profile and brand.
  </Accordion>
</AccordionGroup>

### Option 2: Bring Your Own Twilio Number

If you already have a Twilio number with SMS capabilities enabled, you can integrate it with Retell by following these steps:

<Steps>
  <Step title="Click on Setup SMS Function in Advanced Add-Ons">
    Navigate to your phone number settings in the Retell dashboard and click on the "Setup SMS Function" button under Advanced Add-Ons.
  </Step>

  <Step title="Provide Your Twilio Credentials">
    Enter the following information from your Twilio account:

    * **Account SID**: Your unique Twilio Account identifier
    * **Twilio Auth Token**: Your Twilio authentication token for API access

    <Info>You can find these credentials in your Twilio Console under Account Info.</Info>
  </Step>

  <Step title="Configure SMS Settings">
    Once your credentials are verified, your Twilio number will be integrated with Retell's SMS capabilities. You can then use it for:

    * Sending SMS during calls
    * Setting up two-way SMS conversations (requires enabling `useInboundWebhookOnNumber` on Twilio dashboard for your custom telephony numbers)
  </Step>
</Steps>

<Note>
  * Make sure your Twilio number already has SMS capabilities enabled and is compliant with SMS regulations before integration
  * To enable two-way SMS conversations, enable the `useInboundWebhookOnNumber` option in your phone number configuration on Twilio dashboard
  * For more information about A2P 10DLC compliance, see [Twilio's A2P 10DLC documentation](https://www.twilio.com/docs/proxy/flex-a2p-10dlc)
</Note>

<img />

### Option 3: Use an SMS-Approved Retell Number (No A2P Required)

If you only need to send SMS during active phone calls and want to skip the A2P application entirely, you can send from Retell's **pool of SMS-approved numbers**. No setup or approval steps are needed — select this option when configuring your SMS node or tool, and you can start sending right away. A number from the pool is automatically selected for each call, and all SMS sent within the same call use the same number.

<Warning>
  When sending from an SMS-approved Retell number, the message content is a **preset template provided by Retell** — you cannot customize the text or use a prompt. This option is for in-call SMS only and does not support two-way SMS conversations.
</Warning>

<iframe title="How to send SMS from Retell numbers" />

## Send SMS during call

You can configure agents to send SMS messages to the user during an active phone call. Refer to the following docs for setup details:

* For Conversation Flow: [SMS Node](/build/conversation-flow/sms-node).
* For Single/Multi Prompt: [Send SMS](/build/single-multi-prompt/send-sms).

## Receive SMS during call

Agents can receive and understand SMS messages during an active phone call — even if the agent has not sent any SMS. This allows users to send supplementary information mid-conversation, such as a photo of a document, a screenshot, or a reference number.

For Retell Twilio numbers, this works out of the box without enabling SMS. For custom telephony numbers that have passed A2P applications, this is also supported.

**Multimedia (MMS)** is supported in addition to plain text: users can send images, audio, and video as carrier-supported MMS attachments. Whatever is delivered to Retell as part of the message is incorporated into the ongoing voice conversation so the agent can respond with that context.

<img />

## Set up two way SMS conversation

Once your SMS capability is enabled for the number, you can set up a two way SMS conversation by attaching chat agents to the number, where the number will be able to receive SMS and reply back to user.

<img />

Once the chat agent is attached, the inbound will already work. Inbound webhook can be used to filter and add context to inbound SMS. Read more at [Inbound Webhook](/features/inbound-call-webhook).

For making outbound SMS, you can do that in the dashboard by clicking on the `Make an outbound SMS` button, or use the [Create Outbound SMS API](/api-references/create-sms-chat) to programmatically send it.


# Five9
Source: https://docs.retellai.com/deploy/five9

Five9 is a cloud-based contact center platform that provides inbound and outbound calling, omnichannel engagement, and workforce optimization tools.

<Note>
  Customers with enterprise or paid support plan can contact us via the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com) for step by step guidance to connect with your Five9 contact centre solution.
</Note>

Retell has dedicated SIP trunks with various Five9 PoPs (Points of Presence) that serve live customer traffic. To connect your Five9 trunk with Retell, reach out to your Five9 specialist or contact Retell support via the [Customer Support Portal](https://support.retellai.com/) or at [support@retellai.com](mailto:support@retellai.com).


# Genesys
Source: https://docs.retellai.com/deploy/genesys

A step by step guide to integrate Genesys Cloud with Retell's SIP endpoints to send and receive phone calls.

<Note>
  Customers with an enterprise or paid support plan can contact us via the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com) for step-by-step guidance to connect with your Genesys infrastructure.
</Note>

## Overview

This guide walks through connecting Genesys Cloud to Retell using a **SIP Phone Trunk**. Retell registers with Genesys as a SIP endpoint, allowing Genesys to route inbound calls to Retell agents and allowing Retell to place outbound calls through Genesys numbers.

**Retell SIP details:**

* SIP server URI: `sip.retellai.com`
* IP ranges: `18.98.16.120/30` (all regions), `143.223.88.0/21` (certain US traffic), `161.115.160.0/19` (certain US traffic)
* Recommended transport: TCP (also supports UDP and TLS/SRTP)
* Supported audio codecs: PCMU (G.711 µ-law), PCMA (G.711 A-law), G.722

***

<Steps>
  <Step title="Firewall Considerations">
    Before creating the trunk, ensure your network allows SIP signaling and RTP media between Genesys Cloud and Retell. Genesys Cloud best practice is to specify IP subnets or addresses rather than allowing all traffic — see [About Trunks](https://help.genesys.cloud/articles/about-trunks/) for Genesys security guidance.

    **Whitelist Retell IP ranges (allow inbound SIP from Retell to Genesys):**

    | CIDR Block         | Coverage           |
    | ------------------ | ------------------ |
    | `18.98.16.120/30`  | All regions        |
    | `143.223.88.0/21`  | Certain US traffic |
    | `161.115.160.0/19` | Certain US traffic |

    **Ports to open bidirectionally:**

    | Protocol  | Port        | Purpose                                         |
    | --------- | ----------- | ----------------------------------------------- |
    | TCP / UDP | 8060        | SIP signaling (Genesys SIP phone trunk default) |
    | TCP       | 8061        | SIP over TLS (if using TLS transport)           |
    | UDP       | 16384–32766 | RTP / SRTP media                                |

    <Note>
      Genesys Cloud uses ports **8060** (UDP/TCP) and **8061** (TLS) for SIP phone trunks — different from the standard SIP port 5060/5061. Ensure your firewall and any SBC rules use these Genesys-specific ports.
    </Note>

    **Genesys Cloud media server IPs:**

    Genesys Cloud media traffic originates from AWS regions. Whitelist the IP ranges for your deployed [AWS region](https://help.mypurecloud.com/articles/aws-regions-for-genesys-cloud-deployment/) so Retell's servers can receive RTP from Genesys. Your Genesys Cloud login URL indicates your region (e.g., `login.mypurecloud.com` = US East, `login.mypurecloud.de` = Frankfurt).

    If you are routing calls through an on-premises SBC, apply these rules at the SBC rather than the perimeter firewall.
  </Step>

  <Step title="Create a SIP Phone Trunk in Genesys Cloud">
    A SIP Phone Trunk in Genesys Cloud lets Retell register as a SIP endpoint that Genesys can send calls to and receive calls from. Follow the steps below, or refer to the official [Create a SIP Phone Trunk](https://help.genesys.cloud/articles/create-sip-phone-trunk/) guide.

    1. In Genesys Cloud, go to **Admin** > **Telephony** > **Trunks** (or **Menu** > **Digital and Telephony** > **Telephony** > **Trunks**).

    2. Select the **Phone Trunks** tab.

    3. Click **Create New**.

    4. Enter a name in the **Phone Trunk Name** field (e.g., `Retell-SIP-Trunk`).

    5. Set **Type** to **SIP**.

    6. Verify **Trunk State** is set to **In-Service**.

    7. Under **Protocol and Listen Port**, select your transport and corresponding port:
       * **UDP** or **TCP** → port `8060` (recommended)
       * **TLS** → port `8061` (use this if you require SRTP media encryption)

    8. Under **Registrations**, set the **Max Registration Rate** to limit REGISTER request frequency if required.

    9. Under **SIP Access Control**, configure source IP restrictions:

       * Set **Use Source Address** to **Yes**.
       * Add each Retell IP subnet in CIDR notation:
         * `18.98.16.120/30`
         * `143.223.88.0/21`
         * `161.115.160.0/19`
       * Leave **Always Deny** blank.

       <Note>
         Genesys best practice is to always specify IP subnets here rather than allowing all. This restricts SIP INVITE acceptance to Retell's known IP ranges.
       </Note>

    10. Click **Save Phone Trunk**.

    **Codec configuration:**

    Genesys Cloud supports several codecs on SIP phone trunks (see [SIP Phone Trunk Settings](https://help.genesys.cloud/articles/sip-phone-trunk-settings/)). Configure at least one of the three codecs Retell supports — PCMU is recommended:

    | Codec              | Genesys format | Notes                                   |
    | ------------------ | -------------- | --------------------------------------- |
    | PCMU (G.711 µ-law) | `audio/PCMU`   | Recommended — standard in North America |
    | PCMA (G.711 A-law) | `audio/PCMA`   | Standard outside North America          |
    | G.722              | `audio/G722`   | Wideband (HD voice)                     |

    **TLS / SRTP (optional):**

    If you selected TLS transport, Genesys defaults to TLS v1.2. You can choose from AES-based cipher suites and enable SRTP for media encryption. Mutual TLS authentication is disabled by default. See [SIP Phone Trunk Settings](https://help.genesys.cloud/articles/sip-phone-trunk-settings/) for the full list of TLS and SRTP cipher options.

    **Advanced settings:**

    For call limits, NAT traversal (FENT), inbound digest authentication, and diagnostic captures, refer to [Configure Advanced SIP Phone Trunk Settings](https://help.genesys.cloud/articles/configure-advanced-sip-phone-trunk-settings/). Genesys recommends using defaults unless you have a specific reason to change them.
  </Step>

  <Step title="Configure Phone Numbers to Route Through Retell">
    After creating the trunk, assign or configure phone numbers so inbound calls are directed to Retell and outbound calls from Retell use the correct caller ID.

    **Assign numbers to the SIP trunk:**

    1. Go to **Admin** > **Telephony** > **Phone Numbers**.
    2. Select the number you want to use with Retell.
    3. Edit the number and assign it to the `Retell-SIP-Trunk` you created in Step 2.

    **Import the number into Retell:**

    Retell needs to know the number and how to reach your Genesys trunk for outbound calls.

    1. In the Retell dashboard, go to **Phone Numbers** > **Import Number**.
    2. Fill in the following fields:
       * **Phone Number**: The E.164 format number (e.g., `+12137771234`).
       * **Termination SIP URI**: Your Genesys SIP trunk endpoint. This is the SIP address Retell will dial for outbound calls — typically the FQDN or IP of your Genesys Edge or SBC, on port `8060` (e.g., `your-edge.genesys.com:8060`). Check your Genesys trunk configuration or contact your Genesys admin for the correct address.
       * **SIP Username / Password**: If you configured inbound digest authentication on the Genesys trunk, enter those credentials here.
    3. Save the number and assign a Retell agent to handle calls on it.

    You can also import numbers programmatically via the [Import Number API](/api-references/import-phone-number).

    Once imported, the number appears in your Retell dashboard and you can place and receive calls just like a Retell-purchased number — see [Make Outbound Calls](/deploy/outbound-call) and [Receive Inbound Calls](/deploy/inbound-call).
  </Step>

  <Step title="Configure Inbound Call Routing in Genesys">
    For inbound calls arriving at your Genesys number that should be handled by a Retell agent:

    1. In Genesys Cloud, go to **Admin** > **Routing** > **Call Routing** (or use **Architect** for more complex flows).
    2. Create an **Inbound Call Flow** in Architect that transfers the call to the Retell SIP endpoint:
       * Add a **Transfer to SIP** action.
       * Set the SIP URI to `sip:{call_id}@sip.retellai.com`, where `call_id` comes from a prior call to the [Register Phone Call API](/api-references/register-phone-call).
       * Alternatively, if you imported the number into Retell with the correct termination URI (Step 3), Retell handles call routing automatically when a call is placed to that number — Genesys forwards the SIP INVITE to `sip.retellai.com` via the trunk.
    3. Under **Admin** > **Routing** > **Call Routing**, create a **DID Route** mapping your phone number to this call flow.
    4. Publish the flow.

    **For outbound calls from Retell through Genesys:**

    Use the Retell dashboard or the [Create Phone Call API](/api-references/create-phone-call) to place outbound calls. Retell sends a SIP INVITE to the Genesys termination URI you configured in Step 3, and Genesys routes the call to the PSTN with the assigned number as the caller ID.
  </Step>

  <Step title="TLS and SRTP with Retell">
    Use TLS transport and SRTP media encryption when you need end-to-end signaling and media security between Genesys and Retell. This is optional — TCP is sufficient for most deployments.

    **How it works:**

    * **TLS** encrypts the SIP signaling channel (the INVITE, BYE, etc.).
    * **SRTP** encrypts the RTP audio stream. Retell requires TLS transport to be set in order to use SRTP — you cannot use SRTP over TCP or UDP.

    **Retell SIP URI for TLS:**

    When importing the number into Retell or configuring the termination URI, append the transport parameter:

    ```
    sip:sip.retellai.com;transport=tls
    ```

    **Genesys trunk configuration for TLS:**

    1. In the trunk settings (**Admin** > **Telephony** > **Trunks** > **Phone Trunks** > your trunk), set **Protocol** to **TLS** and **Listen Port** to `8061`.
    2. Under [SIP Phone Trunk Settings](https://help.genesys.cloud/articles/sip-phone-trunk-settings/), configure:
       * **TLS Version**: `TLS v1.2` (Genesys default — matches Retell's supported version).
       * **Cipher Suite**: Choose an AES cipher. Recommended: `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384` or `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`.
       * **Mutual TLS**: Disabled by default. Leave disabled unless your security policy requires client certificate authentication from Retell. If you need mutual TLS, contact the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com) as this requires coordination with Retell's infrastructure team.
    3. Enable **SRTP** under the media/security settings. Genesys supports the following SRTP cipher suites, all of which Retell accepts:
       * `AES_CM_128_HMAC_SHA1_80` (recommended)
       * `AES_CM_128_HMAC_SHA1_32`
       * `AES_CM_256_HMAC_SHA1_80`
       * `AES_CM_256_HMAC_SHA1_32`

    **Firewall for TLS:**

    Ensure port `8061` (TCP) is open bidirectionally between Retell's IP ranges and your Genesys Cloud edge, in addition to the RTP media ports.

    | Protocol | Port        | Purpose                        |
    | -------- | ----------- | ------------------------------ |
    | TCP      | 8061        | SIP over TLS                   |
    | UDP      | 16384–32766 | SRTP media (same ports as RTP) |

    <Note>
      Retell's SIP server presents a certificate signed by the **Amazon Trust Services** CA (Amazon runs Retell's infrastructure). Genesys Cloud validates this automatically for most deployments. If certificate validation fails and calls do not connect — particularly when an on-premises SBC or Edge device is in the path — you may need to install Retell's Root CA on that device.

      Download the following certificates from the [Amazon Trust Services repository](https://www.amazontrust.com/repository/) and install them in the trusted CA store of your Genesys Edge or SBC:

      * **Root CA**: Amazon Root CA 1 (`AmazonRootCA1.pem`)
      * **Intermediate CA** (optional, install if your device requires the full chain): `C=US, O=Amazon, CN=Amazon RSA 2048 M01`

      The intermediate certificate is typically not required if your device performs online certificate chain validation, but some on-premises SBCs and Edge appliances require the full chain to be pre-installed locally. If you see TLS handshake failures with an "unknown CA" or "incomplete chain" error, install both the root and the intermediate.

      Also check that your SBC is not intercepting TLS with its own self-signed certificate before forwarding to Retell, as this will cause validation to fail on Retell's side.
    </Note>
  </Step>

  <Step title="Test the Integration">
    **Inbound test (external call → Genesys number → Retell agent):**

    1. Call the number assigned to the `Retell-SIP-Trunk` from an external phone.
    2. Confirm the call appears in Retell's **Calls** dashboard and is handled by the correct agent.
    3. Verify bidirectional audio and that the call completes cleanly.

    **Outbound test (Retell → Genesys → PSTN):**

    1. Initiate an outbound call from the Retell dashboard or API using the imported number.
    2. Confirm the receiving party sees the correct caller ID.
    3. Check audio quality in both directions.
  </Step>

  <Step title="Debug Call Issues on Genesys">
    If calls fail or have audio problems, use the following tools.

    **1. Interaction Detail Records**

    Go to **Performance** > **Workspace** > **Interactions** (or **Contact Center** > **Interactions**). Search by ANI, DNIS, or time range. Click an interaction to see the full SIP event timeline, call path, and any error codes:

    * `403 Forbidden` → SIP access control mismatch; verify Retell IP subnets are whitelisted on the trunk.
    * `404 Not Found` → Incorrect SIP URI or trunk routing misconfiguration.
    * `503 Service Unavailable` → Retell SIP server unreachable; check DNS for `sip.retellai.com` and firewall rules.

    **2. Trunk Status**

    Go to **Admin** > **Telephony** > **Trunks** > **Phone Trunks** and check the status of `Retell-SIP-Trunk`. A **Down** or **Degraded** state indicates a connectivity or registration problem. Verify firewall rules and that Retell's IPs are correctly added to SIP Access Control.

    **3. Protocol Capture (SIP Trace)**

    Enable protocol capture under [Advanced SIP Phone Trunk Settings](https://help.genesys.cloud/articles/configure-advanced-sip-phone-trunk-settings/) in the **Diagnostic** section. Use this together with Genesys Cloud Technical Support to inspect raw SIP messages. Look for:

    * Codec mismatch in SDP offer/answer — ensure at least one common codec (e.g., PCMU) is in both Genesys and Retell's codec lists.
    * Missing or rejected `Contact` / `Via` headers.
    * Authentication challenges (401/407) — configure inbound digest auth credentials consistently on both sides.
    * NAT issues — if Genesys is behind NAT, enable Far-End NAT Traversal (FENT) in the transport section of advanced trunk settings.

    **4. One-Way or No Audio**

    One-way audio is almost always a firewall or NAT issue blocking RTP in one direction:

    * Confirm UDP 16384–32766 is open bidirectionally between Genesys media servers and Retell's IP ranges.
    * Check the SIP trace SDP `c=` and `m=` lines to confirm the IP address and port Genesys is advertising for media.
    * Verify Retell received and is sending audio by checking the call in the Retell dashboard.

    **5. Quick Reference**

    | Symptom                  | Likely Cause                             | Fix                                             |
    | ------------------------ | ---------------------------------------- | ----------------------------------------------- |
    | Call not reaching Retell | Trunk misconfigured or firewall blocking | Check SIP Access Control IPs and firewall rules |
    | 403 Forbidden            | IP not whitelisted on trunk              | Add Retell CIDR blocks to SIP Access Control    |
    | 503 Service Unavailable  | `sip.retellai.com` unreachable           | Check DNS resolution and firewall on port 8060  |
    | One-way audio            | RTP blocked or NAT issue                 | Open UDP 16384–32766, check SDP IPs in trace    |
    | No audio (codec)         | No shared codec in SDP                   | Add PCMU/PCMA to Genesys trunk codec list       |
    | Call drops at \~30s      | Mid-call SIP re-INVITE blocked           | Allow mid-call signaling through firewall       |
    | Call drops on register   | Max Registration Rate too low            | Increase Max Registration Rate on trunk         |

    <Note>
      If you cannot resolve the issue, capture the Genesys Interaction ID and the Retell Call ID (from the Retell dashboard) and contact the <a href="https://support.retellai.com/">Customer Support Portal</a> or [support@retellai.com](mailto:support@retellai.com).
    </Note>
  </Step>
</Steps>


# Receive calls
Source: https://docs.retellai.com/deploy/inbound-call

A step by step guide to receive phone calls with Retell managed numbers & imported numbers

### Bind Voice Agents

* Only when you bind agents to a number will the number be able to receive and make calls.
* You can assign different inbound and outbound agent to the number.
* You can leave agent unset to disable inbound / outbound (for example, you are doing outbound and don't
  want callbacks, you can leave `inbound_agent_id` unset)

<Frame>
  <img alt="Phone number configuration showing agent binding for inbound and outbound" />
</Frame>

After binding an agent for inbound, you should be able to receive inbound calls already.

### Handle inbound overflow

Inbound calls count toward your workspace concurrency limit. To keep inbound calls available during
high outbound volume, you can reserve part of your concurrency for inbound calls. See
[Reserved Inbound Concurrency](/deploy/concurrency#reserved-inbound-concurrency).

If all concurrency slots are in use, Retell briefly waits for a slot to open. If no slot opens after
about 40 seconds, Retell transfers the call to the phone number's `fallback_number` when one is
configured. Without a fallback number, the call ends with `concurrency_limit_reached`.

### A/B Testing

See [A/B Testing](/deploy/ab-testing).

### Inbound Call Webhook

A lot of times, you want to use different agents to handle inbound calls of a number; also you need a way to provide dynamic variables to use for inbound calls, and other fields specific to that call.

Read more at [Inbound Call Webhook](/features/inbound-call-webhook)

### Inbound Custom SIP Headers

* You can use custom SIP headers to pre-set dynamic variables for a call.
* Retell extracts any header starting with `sip.h.x-`, along with common SIP headers like `Diversion`, `History-Info`, `User-To-User` and `P-Asserted-Identity`, and converts each into a dynamic variable by stripping the `sip.h.` prefix.
  * E.g. `sip.h.x-caller: abc` -> `x-caller: abc`
  * E.g. `sip.h.p-asserted-identity: +12345678910` -> `p-asserted-identity: +12345678910`
  * E.g. `sip.h.diversion: <sip:2000@192.168.254.254>;privacy=off;reason=no-answer;counter=1;screen=no` -> `diversion: <sip:2000@192.168.254.254>;privacy=off;reason=no-answer;counter=1;screen=no`

### Get Call Detail

* API: You can use [Get Call API](/api-references/get-call) to get information like
  transcript, recording, latency tracking, etc.
* Webhook: You can also setup webhooks to receive real time updates when call is
  initiated, ends, and analyzed.
  Read more at [Call Webhook Guide](/features/webhook-overview#event-types).


# International Calling and Fees
Source: https://docs.retellai.com/deploy/international-call



You can use Retell numbers to call US and international numbers.
Below is the list of supported countries along with their respective rates.

Retell also offers international numbers. See our [Purchase Number page](/deploy/purchase-number) for more details.

<Steps>
  <Step title="Twilio">
    | 🌍 Country          | 💬 Rate/Min |
    | :------------------ | ----------- |
    | 🇺🇸 US             | \$0.015     |
    | 🇺🇸 US (Toll-Free) | \$0.06      |
    | 🇮🇳 India          | \$0.15      |
    | 🇦🇺 Australia      | \$0.10      |
    | 🇩🇪 Germany        | \$0.10      |
    | 🇪🇸 Spain          | \$0.10      |
    | 🇬🇧 UK             | \$0.10      |
    | 🇲🇽 Mexico         | \$0.05      |
    | 🇫🇷 France         | \$0.06      |
    | 🇯🇵 Japan          | \$0.28      |
    | 🇨🇦 Canada         | \$0.03      |
    | 🇮🇹 Italy          | \$0.06      |
    | 🇮🇩 Indonesia      | \$0.40      |
    | 🇵🇭 Philippines    | \$0.80      |
    | 🇲🇾 Malaysia       | \$0.20      |
    | 🇹🇭 Thailand       | \$0.45      |
  </Step>

  <Step title="Telnyx">
    | 🌍 Country  | 💬 Rate/Min |
    | ----------- | ----------- |
    | 🇺🇸 US     | \$0.03      |
    | 🇮🇳 India  | \$0.25      |
    | 🇨🇦 Canada | \$0.03      |
  </Step>
</Steps>


# Create Batch calls
Source: https://docs.retellai.com/deploy/make-batch-call

Create, schedule, and monitor batch calls in bulk.

### Overview

Batch calls enable you to efficiently manage multiple calls by organizing them into groups. You can create, schedule, and monitor calls in bulk, streamlining communication workflows. This feature is particularly useful for campaigns, updates, or any situation requiring multiple recipients to be contacted.

## Create a batch call

<Steps>
  <Step title="Click Create Batch Call">
    Navigate to the Batch Call tab in the Retell AI workspace and click the "Create Batch Call" button located in the top-right corner.

    <Frame>
      <img alt="Batch call page with Create Batch Call button" />
    </Frame>
  </Step>

  <Step title="Enter call name and phone number">
    * Provide a unique name for the batch call to differentiate it from others
    * Select the "From Number" from the dropdown menu
    * Ensure the number is bound to agents to enable batch calls
  </Step>

  <Step title="Upload CSV">
    * Prepare your recipient list in CSV format with a header row including a "phone number" column
    * Use the provided CSV template by clicking "Download the template," or upload your custom file

    <Frame>
      <img alt="Batch call editor with agent and CSV settings" />
    </Frame>

    * For dynamic variables, add additional columns in the CSV with custom data for each recipient (e.g., a column header `first_name` can be referenced as `{{first_name}}`)
    * If the number to call is not in e.164 format, you can choose to ignore e.164 validation by adding a column to the CSV named `ignore e164 validation` with value `true`. This only applies when you are using custom telephony and does not apply when you are using Retell Telephony.

    The CSV also supports the following optional columns:

    * `override agent id`: Override the agent used for this particular call.
    * `override agent version`: Override the agent version for this particular call.
    * `metadata`: A JSON string to store arbitrary data with the call (e.g., `{"customer_id":"cust_123"}`).
    * `custom_sip_headers`: A JSON string of custom SIP headers, keys must start with `X-` (e.g., `{"X-Custom-Header":"value"}`).
    * Any other columns are treated as dynamic variables injected into your Response Engine prompt and tool descriptions.

    <Frame>
      <img alt="CSV column for ignoring E.164 validation" />
    </Frame>
  </Step>

  <Step title="Configure the time window">
    * Open the configuration modal to define the batch call time windows

    <Frame>
      <img alt="Batch call time window configuration modal" />
    </Frame>
  </Step>

  <Step title="Create now or schedule">
    * Choose between "Send Now" to start the calls immediately or "Schedule" for a future time
    * Click "Save as Draft" to revisit later or "Send" to initiate or schedule the calls
  </Step>
</Steps>

## Monitor batch calls

### Batch call status

Once your batch calls are created, you can monitor their progress and history in the Batch Call tab. Batch calls are classified by their status:

* <b>Draft</b>: Editable and unsent. Drafts will not trigger any calls until submitted.
* <b>Planned</b>: Scheduled for a future time. These cannot be edited once scheduled.
* <b>Ongoing</b>: Currently in progress, with calls initiated as concurrency slots become available.
* <b>Sent</b>: All calls in the batch have been successfully completed.

### Batch call metrics

You can view the following metrics:

* <b>Sent</b>: Total calls sent from the batch.
* <b>Picked Up</b>: Number of calls answered by recipients.
* <b>Successful</b>: Calls successfully completed based on the predefined criteria.

<Frame>
  <img alt="Batch call list with status and metrics" />
</Frame>

### Call details

Click the history icon to view the call details of each call in the batch.

<Frame>
  <img alt="Individual call details within a batch" />
</Frame>


# Outbound Calls (Make Calls)
Source: https://docs.retellai.com/deploy/outbound-call

Step-by-step guide to configure agents and make outbound phone calls using Retell

## Overview

This guide covers how to make outbound calls with your Retell agents. Before proceeding, ensure you have:

* Created and configured an agent
* Purchased or imported phone numbers
* Set up your API credentials

## Prerequisites

* **Phone Number**: A Retell-managed or imported number
* **Agent**: A configured agent ready for outbound calls
* **API Key**: Your Retell API key for authentication

## Step 1: Bind Agents to Phone Numbers

Before making calls, you must assign agents to your phone numbers. This configuration determines how your number handles both inbound and outbound calls.

### Configuration Options

| Setting            | Purpose                                 | Use Case                      |
| ------------------ | --------------------------------------- | ----------------------------- |
| **Inbound Agent**  | Handles incoming calls to this number   | Customer support, callbacks   |
| **Outbound Agent** | Used when making calls from this number | Sales outreach, notifications |

### Flexible Agent Assignment

* **Different agents**: Use specialized agents for inbound vs outbound
* **Outbound only**: Leave inbound agent unset to prevent callbacks
* **Inbound only**: Configure only inbound agent for receive-only numbers

<Frame>
  <img alt="Phone number configuration showing inbound and outbound agent assignment" />
</Frame>

<Tip>
  After binding an inbound agent, your number is immediately ready to receive calls. Test it by calling the number!
</Tip>

### A/B Testing

See [A/B Testing](/deploy/ab-testing).

## Step 2: Make Outbound Calls

### International Calling Restrictions

<Warning>
  **Retell-purchased numbers**: Retell supports calling to [15 countries](/deploy/international-call).

  **Imported numbers**: International calling depends on your telephony provider's settings.
</Warning>

### Call Parameters

When making outbound calls (v2), these parameters are supported:

| Parameter                      | Type           | Example                         | Description                                                             |
| ------------------------------ | -------------- | ------------------------------- | ----------------------------------------------------------------------- |
| `from_number`                  | string (E.164) | `+14157774444`                  | Your Retell-managed or imported number.                                 |
| `to_number`                    | string (E.164) | `+12137774445`                  | Destination number.                                                     |
| `override_agent_id`            | string         | `agent_abc123`                  | Override the agent used for this call (optional).                       |
| `override_agent_version`       | integer        | `1`                             | Version of the override agent; defaults to latest if omitted.           |
| `agent_override`               | object         | See below                       | Per-call partial overrides for agent/response engine (optional).        |
| `metadata`                     | object         | `{ "customer_id": "cust_123" }` | Free-form metadata stored with the call (size limit applies).           |
| `retell_llm_dynamic_variables` | object         | `{ "name": "John" }`            | Key–value strings injected into prompts/tools (optional).               |
| `custom_sip_headers`           | object         | `{ "X-Call-ID": "123" }`        | Outbound SIP headers forwarded to your provider (optional).             |
| `ignore_e164_validation`       | boolean        | `false`                         | Only for custom telephony. Bypass E.164 validation for special routing. |

Agent overrides let you adjust per-call behavior without changing the saved agent. See “Agent Overrides” in the [Create Phone Call API](/api-references/create-phone-call) for supported fields and examples.

<Frame>
  <img />
</Frame>

### API Implementation

For complete parameter documentation, see [Create Phone Call API Reference](/api-references/create-phone-call).

<CodeGroup>
  ```typescript Node theme={null}
  const registerCallResponse = await retell.call.createPhoneCall({
    from_number: '+14157774444', // replace with the number you purchased
    to_number: '+12137774445',  // replace with the number you want to call
    // Optional: per-call agent selection and overrides
    override_agent_id: 'agent_abc123',
    override_agent_version: 0, // or omit to use latest
    agent_override: {
      agent: {
        voice_speed: 1.1,
        enable_backchannel: true,
      },
      // retell_llm or conversation_flow overrides are also supported
    },

    retell_llm_dynamic_variables: { // dynamic variables (optional, string values only)
      name: 'John Doe',
      blood_group: 'B+'
    },  
    custom_sip_headers: { // replace with custom sip headers you want to send (optional)
      X-Custom-Header: 'Custom Value'
    }
  });
  console.log(registerCallResponse);
  ```

  ```python Python theme={null}
  # Initiate an outbound call using the newly created agent
  call = client.call.create_phone_call(
      from_number="+14157774444", # replace with the number you purchased
      to_number="+12137774445",  # replace with the number you want to call
      # Optional: per-call agent selection and overrides
      override_agent_id="agent_abc123",
      override_agent_version=0,  # or omit to use latest
      agent_override={
        "agent": {
          "voice_speed": 1.1,
          "enable_backchannel": True,
        }
      },

      retell_llm_dynamic_variables={ # dynamic variables (optional, string values only)
        name: 'John Doe',
        blood_group: 'B+'
      },
      custom_sip_headers={ # replace with custom sip headers you want to send (optional)
        X-Custom-Header: 'Custom Value'
      }
  )
  print(call)
  ```
</CodeGroup>

## Step 3: Configure CPS (Calls Per Second)

### Understanding CPS Limits

CPS (Calls Per Second) controls how many outbound calls you can initiate per second. This prevents system overload and ensures call quality.

### Default Limits & Scaling

| Provider             | Default CPS | Maximum CPS | Notes                                                                        |
| -------------------- | ----------- | ----------- | ---------------------------------------------------------------------------- |
| **Twilio**           | 1           | 5           | Changes take up to 10 minutes                                                |
| **Telnyx**           | 1           | 16          | Instant updates                                                              |
| **Custom Telephony** | 1           | 150         | Check your custom provider's SIP trunk capacity before increasing this limit |

### Important Considerations

1. **Throttling Protection**: Exceeding limits results in rejected calls
2. **Gradual Scaling**: Start low and increase based on actual needs
3. **Provider Limits**: Your telephony provider may have additional restrictions
4. **Cost Impact**: Higher CPS may increase telephony costs

<div>
  <Frame>
    <img />
  </Frame>
</div>

### Best Practices for High-Volume Calling

<Tip>
  **Implement retry logic** with exponential backoff to handle throttling gracefully:

  ```javascript theme={null}
  // Example retry logic
  const maxRetries = 3;
  let retryDelay = 1000; // Start with 1 second

  for (let i = 0; i < maxRetries; i++) {
    try {
      await makeCall();
      break;
    } catch (error) {
      if (error.code === 'rate_limited') {
        await sleep(retryDelay);
        retryDelay *= 2; // Exponential backoff
      }
    }
  }
  ```
</Tip>

## Step 4: Monitor Call Details

### Available Monitoring Methods

#### 1. API Polling

Use [Get Call API](/api-references/get-call) to retrieve:

* Full transcript
* Call recording
* Latency metrics
* Function call logs
* Call duration and status

#### 2. Real-time Webhooks

Set up [webhooks](/features/webhook-overview#event-types) to receive instant notifications for:

* **Call Started**: When the call connects
* **Call Ended**: Final status and duration
* **Call Analyzed**: Transcript and analysis ready
* **Call Failed**: Error details and reasons

<Note>
  Webhooks provide real-time updates without polling, making them ideal for production systems.
</Note>

<b>Triggering Outbound Calls (Using Make.com)</b>

<iframe title="YouTube video player" />

### Additional Resources

* [Community Templates](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope): Real-world outbound calling examples
* [Batch Calling Guide](/deploy/make-batch-call): For high-volume campaigns
* [Webhook Setup](/features/webhook-overview): Configure real-time notifications


# Purchase phone number
Source: https://docs.retellai.com/deploy/purchase-number

A step by step guide to buy a number from Retell

This guide will walk through how to purchase a number from Retell. The numbers
are managed by Retell, so you don't have to worry about the telephony infrastructure.

<Note>Currently we only support purchase of US and Canada numbers and support making calls to [15 countries](/deploy/international-call). If you are looking to use numbers from other countries, or to make calls to more countries, or to use your own telephony provider, check out [Custom Telephony guide](/deploy/custom-telephony).</Note>

### From Dashboard

You can purchase and bind agents to the number from the dashboard. You can optionally specify the
area codes you want to purchase from.

<img />

After the number is purchased, you can change its nickname so that it's easier for you to find and identify.

<img />

At this stage, the number should already be ready to accept inbound calls if you have assigned an inbound agent.
Give it a try by calling it!

### From API

Check out [Create Phone Number API Reference](/api-references/create-phone-number)
for all the parameters you can use programmatically.

* Phone numbers are yours once purchased, and can be used indefinitely.
  Find numbers you own [here](/api-references/list-phone-numbers).
* You can assign different inbound and outbound agent to the number.
* If you don't want user to be able to call this number (maybe you are doing outbound and don't
  want callbacks), you can leave `inbound_agent_id` unset.

<CodeGroup>
  ```typescript Node theme={null}
  const phoneNumberResponse = await retell.phoneNumber.create({
    inbound_agent_id: "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD", // replace with the agent id you want to assign
    outbound_agent_id: "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD", // replace with the agent id you want to assign
  });

  console.log(phoneNumberResponse);
  ```

  ```python Python theme={null}
  # Purhcase a phone number
  phone_number = client.phone_number.create(
    inbound_agent_id="oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD", # replace with the agent id you want to assign
    outbound_agent_id: "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD", # replace with the agent id you want to assign
  )
  print(phone_number)
  ```
</CodeGroup>

### Pricing

We support both **Twilio** and **Telnyx** numbers:

* **Twilio**
  * US numbers: **\$2/month**
  * US toll-free numbers: **\$5/month**
  * Canadian numbers: **\$2/month**
* **Telnyx**
  * US numbers only: **\$2/month**

> ⚠️ **Note:** Toll-free numbers cost \$0.06 per minute for inbound calls. Outbound calls are charged at the same rate as regular U.S. numbers.


# Telnyx
Source: https://docs.retellai.com/deploy/telnyx

A step by step guide to connect to your Telnyx account via SIP trunking

<Steps>
  <Step title="Create Elastic SIP Trunking">
    1. Create the trunk, select FQDN as the type, and give it a name.

    <img />

    2. Add FQDN

    Add the FQDN of Retell's SIP server: `sip.retellai.com`. Select `SRV` as the
    DNS record type.

    <img />

    3. Setup Outbound Calls Authentication

    Select credentials as the authentication method, and add the username and password.
    You will need to use this username and password when importing the number to Retell.

    <img />

    <Note>
      Telnyx requires the header `X-Telnyx-Username: <username>` to be included in the outbound calls when using credentials as the authentication mechanism.
      See Telnyx [documentation](https://support.telnyx.com/en/articles/5271423-guide-to-sip-anchorsite-settings#h_0b59d6992a) for more details.
      You can find details on adding custom SIP headers on [Make Outbound Calls](/deploy/outbound-call#step-2:-make-outbound-calls) page.
    </Note>

    4. Setup Inbound Setting

    * Select `+E.164` as the number format.
    * Select `G722`, `G711U`, `G711A` as the codecs.
    * Select `TCP` as the transport method. (TCP is recommended over UDP due to reliability factors)
    * Select your SIP region.

    <img />

    4. Setup Outbound Setting

    Create a new outbound voice profile

    <img />

    And select that in the outbound setting

    <img />
  </Step>

  <Step title="Move numbers to Elastic SIP Trunking">
    You've created the elastic SIP trunk, now you would need to purchase numbers / move
    existing numbers to this trunk.

    <img />
  </Step>

  <Step title="Import numbers to Retell">
    Now the number is set up with your elastic SIP trunking, you need to
    import the number to Retell so that we will know how to route the call.

    <img />

    Here you will supply Telnyx's FQDN as the termination SIP URI. You can find your FQDN based on
    your choice of SIP region in this [doc](https://sip.telnyx.com/) (e.g. sip.telnyx.com). You will also need to supply
    the username, password and any additional SIP headers you set up earlier in the outbound authentication as well.

    <img />

    You can also import number programmatically via [Import Number API](/api-references/import-phone-number).

    Now the number is imported, you can make and receive calls with this number just like a number
    you purchased from Retell -- it will show up in your dashboard, and you can make phone calls from
    Dashboard directly. You can also use the [Create Phone Call API](/api-references/create-phone-call)
    to create calls programmatically.
    If you wish to Retell to stop using this number, you can delete it from the dashboard or via
    the [Delete Number API](/api-references/delete-phone-number).
  </Step>
</Steps>


# Twilio
Source: https://docs.retellai.com/deploy/twilio

A step by step guide to connect to your Twilio account via SIP trunking

## Steps

<Steps>
  <Step title="Create Elastic SIP Trunking">
    1. Create the trunk, give it a name, and toggle some general settings

    <img />

    2. Setup termination (this is for outbound)

    * the termination SIP URI here is important, we would use it in later steps. You might want to use a localized termination uri that's near your region. You can expand and view your localized uris in the twilio console.

    <img />

    * For your elastic SIP trunk to accept our outbound request, you need to whitelist
      IP address or create a auth with username and password.
      * If you opt for the auth route, you need to specify the username and password
        in the next step when importing the number to Retell.
      <img />
      * You need to whitelist Retell SIP SBC CIDR block 18.98.16.120/30 like following:
      <img />

    3. Setup origination (this is for inbound)

    * Here you will specify Retell's SIP server address as the origination SIP URI:
      `sip:sip.retellai.com`.

    <img />
  </Step>

  <Step title="Move numbers to Elastic SIP Trunking">
    You've created the elastic SIP trunk, now you would need to purchase numbers / move
    existing numbers to this trunk.

    <img />
  </Step>

  <Step title="Import numbers to Retell">
    Now the number is set up with your elastic SIP trunking, you need to
    import the number to Retell so that we will know how to route the call.

    <img />

    Here you will supply the termination SIP URI you set up in Step 1. If you have set up
    auth via credentials, you will need to supply the username and password as well.

    <img />

    You can also import number programmatically via [Import Number API](/api-references/import-phone-number).

    Now the number is imported, you can make and receive calls with this number just like a number
    you purchased from Retell -- it will show up in your dashboard, and you can make phone calls from
    Dashboard directly. You can also use the [Create Phone Call API](/api-references/create-phone-call)
    to create calls programmatically.
    If you wish to Retell to stop using this number, you can delete it from the dashboard or via
    the [Delete Number API](/api-references/delete-phone-number).
  </Step>
</Steps>

## Common Issues

**1. After connecting, inbound works but outbound does not work?**

* Check your Termination SIP URI
  If there's a space in it, please remove. Also you should use a localized termination uri that's near your region. Check out this [doc](https://www.twilio.com/docs/global-infrastructure/localized-uris/termination) to select one.

* Check your user name and credentials
  Please make sure you entered the right user name and credentials which shows in this dialog.
  Please note the user name is not the friendly name that shows in the credential list.
  The friendly name is different to user name, you need to double check if you happen to give a different name.

<img />

**2. How do I set up dialing to international countries?**

* Search "geo" to find the "Voice Geographic Permissions" setting.
  <img />

* Choose "Elastic Sip Trunking" in selector, and select the countries you would like to dial.
  <img />

## Phone Number Masking

If you have a personal phone number or a trusted business number you would like to display to the callee, verified phone numbers can be imported into Twilio to serve as the caller ID.

### Add a Caller ID

1. Go to the [Verified Caller IDs page](https://www.twilio.com/console/phone-numbers/verified?_gl=1*l511c3*_gcl_aw*R0NMLjE3NTQ0MTE4NjUuQ2p3S0NBancxZExEQmhCb0Vpd0FRTlJpUVk5QWVqRDFrc2hEZl9ycVdOVlI4bmR3RVNTei1nM3JBcGpORVFXX3BCLXdMRFZPTnM3ei14b0NWNmdRQXZEX0J3RQ..*_gcl_au*MTAzNDAwNDYyNi4xNzUyNTE4OTQy*_ga*MjA5ODY1MzAyMS4xNzUyNTE4OTQy*_ga_RRP8K4M4F3*czE3NTczNzcyODAkbzI0JGcxJHQxNzU3MzgwOTUxJGo2MCRsMCRoMA..)
2. Click **Add a new Caller ID**
3. Enter the desired phone number to verify, select the desired verification method, and then click **Verify Number**

<img />

4. The number entered will receive an OTP Authentication code for verification. Enter this verification code on the next window.

<img />

5. Once you click **Submit**, if the correct OTP code was entered, you will receive a **Successful** notification and the number will be added to your account as a verified caller ID.

### Configure SIP Header Rules to Display Caller ID

1. In the Twilio Console, navigate to Elastic SIP Trunking → Trunks → \[your trunk] → Termination
2. Scroll down to Header Manipulation and open **View all SIP header manipulation policies**

<img />

3. Click on **Create a policy** in the top right and give your policy a friendly name
4. Click on **+ Add request rule** and give the rule a friendly name
5. Under the Actions section, set the following values:
   * **SIP header field**: **From number**
   * **Action**: **Replace with**
   * **Value**: Your caller ID in E.164 format (e.g. +18881230987)

<img />

6. Click **Add rule**, and then click **Save policy**
7. Return to the Termination tab within your trunk, and select the new header manipulation policy from the dropdown
8. Now, any number imported from this Twilio trunk into your Retell account will use your verified caller ID. Place an outbound test call to validate the changes.
   * *Note:* You will need at least one number purchased from Twilio in your SIP trunk in order to apply the caller ID


# Vonage
Source: https://docs.retellai.com/deploy/vonage

A step by step guide to connect to your Vonage account via SIP trunking

<Steps>
  <Step title="Create Elastic SIP Trunking">
    1. Locate the SIP section in the Vonage dashboard, and select "Something else" for the provider type.

    <img />

    <img />

    From here, you can follow these instructions step by step.

    2. Setup termination (for outbound)

    * the termination SIP URI and the username and password here is important, we would use it in later steps, please take notes of it.

    <img />

    3. Setup origination (for inbound)

    * Here you will specify Retell's SIP server address as the origination SIP URI:
      `sip.retellai.com`.

    <img />
  </Step>

  <Step title="Move numbers to Elastic SIP Trunking">
    You've created the elastic SIP trunk, now you would need to purchase numbers / link
    existing numbers to this trunk.

    <img />
  </Step>

  <Step title="Import numbers to Retell">
    Now the number is set up with your elastic SIP trunking, you need to
    import the number to Retell so that we will know how to route the call.

    Here you will supply the termination SIP URI, the username and password you set up in Step 1.

    <img />

    You can also import number programmatically via [Import Number API](/api-references/import-phone-number).

    Now the number is imported, you can make and receive calls with this number just like a number
    you purchased from Retell -- it will show up in your dashboard, and you can bind agents, make phone calls from
    Dashboard directly.

    Check out the [Make phone call](/deploy/outbound-call) guide to learn how to make phone calls.
  </Step>
</Steps>


# Connect to web call
Source: https://docs.retellai.com/deploy/web-call

A step by step guide to create a web call with agent using frontend Web SDK

### Set up the SDK

Step 1: Install the Retell Web SDK

`npm install retell-client-js-sdk`

Step 2: Set up the SDK class

```javascript theme={null}
import { RetellWebClient } from "retell-client-js-sdk";

const retellWebClient = new RetellWebClient();
```

### Call `create-web-call` to get call id

Your client code should call your server endpoint which internally calls
[create web call](https://docs.retellai.com/api-references/create-web-call) to get the
access token for the call. The endpoint requires using your Retell API Key, which is the
reason why you need to call the endpoint from the server instead of client to
protect the key from exposing.

The access token obtained will be used in your frontend client code to start the call.

<Warning>Note that if you do not start the call within 30s obtaining the access
token, we will invalidate it and the call will be marked with error.</Warning>

### Start the Call

Once call starts, you can listen to a couple events that's emitted for real time
updates about the call.

```javascript theme={null}
await retellWebClient.startCall({
  accessToken: createCallResponse.access_token,
});
```

There are other optional options that allow you to set the sample rate of call,
audio capture and playback device, whether to receive raw audio bytes from the
client.

```javascript theme={null}
await retellWebClient.startCall({
  accessToken: createCallResponse.access_token,
  sampleRate: 24000, // (Optional) set sample rate of the audio capture and playback
  // (Optional) device id of the mic.
  captureDeviceId: "default",
  // (Optional) device id of the speaker
  playbackDeviceId:
    "0ec1807fd0fe6e51b990660ec4e2ebb78sdfcba51e279815d00c423ce03407ff",
  // (Optional) Whether to emit "audio" events that contain raw pcm audio bytes represented by Float32Array
  emitRawAudioSamples: false,
});
```

### Stop the Call

You can close a web call with the agent by using

```javascript theme={null}
retellWebClient.stopCall();
```

### Listen to events

You can listen to events emitted by the SDK to get real time updates about the call, including
who is speaking, the real time transcript, start and end of the call.

```javascript theme={null}
retellWebClient.on("call_started", () => {
  console.log("call started");
});

retellWebClient.on("call_ended", () => {
  console.log("call ended");
  setIsCallActive(false);
});

// When agent starts talking for the utterance
// useful for animation
retellWebClient.on("agent_start_talking", () => {
  console.log("agent_start_talking");
});

// When agent is done talking for the utterance
// useful for animation
retellWebClient.on("agent_stop_talking", () => {
  console.log("agent_stop_talking");
});

// Real time pcm audio bytes being played back, in format of Float32Array
// only available when emitRawAudioSamples is true
retellWebClient.on("audio", (audio) => {
  // console.log(audio);
});

// Update message such as transcript
// You can get the transcript with update.transcript
// Please note that transcript only contains last 5 sentences to avoid the payload being too large
retellWebClient.on("update", (update) => {
  // console.log(update);
});

retellWebClient.on("metadata", (metadata) => {
  // console.log(metadata);
});

retellWebClient.on("error", (error) => {
  console.error("An error occurred:", error);
  // Stop the call
  retellWebClient.stopCall();
});
```

### Audio Basics

If you have not worked with audio bytes before, we strongly suggest you check
out [audio basics](/knowledge/audio-basics), which can help with choosing the
best configuration here.

PCM audio format conversion functions `convertUnsigned8ToFloat32` and
`convertFloat32ToUnsigned8` can be found in
[audio basics](/knowledge/audio-basics#pcm-audio-representation).


# Deprecated on 01/23/2026
Source: https://docs.retellai.com/deprecation-notice/2026/01-23_cold_transfer_mode_selection



## Cold Transfer Mode Selection

The behavior of the `show_transferee_as_caller` parameter in Cold Transfer options is changing. Previously, this parameter was used to toggle between SIP REFER and SIP INVITE transfer modes.

**Affected APIs:**

* [Create Retell LLM](/api-references/create-retell-llm)
* [Update Retell LLM](/api-references/update-retell-llm)
* [Create Conversation Flow](/api-references/create-conversation-flow)
* [Update Conversation Flow](/api-references/update-conversation-flow)
* [Create Conversation Flow Component](/api-references/create-conversation-flow-component)
* [Update Conversation Flow Component](/api-references/update-conversation-flow-component)

**What's changing:**

* The `show_transferee_as_caller` parameter will no longer control the transfer mode (SIP REFER vs SIP INVITE).
* Use the new `cold_transfer_mode` parameter to explicitly choose between `sip_refer` and `sip_invite`.
* The `show_transferee_as_caller` parameter will only control caller ID display and will only take effect when `cold_transfer_mode` is set to `sip_invite`.

**Migration:**

* Set `cold_transfer_mode` to `sip_refer` or `sip_invite` to choose the transfer method.
* Set `show_transferee_as_caller` to `true` only if you want to show the transferee as the caller when using `sip_invite` mode.

**Effective date:** After 01/23/2026, `show_transferee_as_caller` will no longer affect the transfer mode selection.


# Deprecated on 03/31/2026
Source: https://docs.retellai.com/deprecation-notice/2026/03-31_phone_number_agent_fields



## Phone number single-agent fields

The single-agent fields on phone number configuration are deprecated in favor of weighted agent lists for inbound/outbound calls and SMS.

**Affected APIs:**

* [Create Phone Number](/api-references/create-phone-number)
* [Import Phone Number](/api-references/import-phone-number)
* [Update Phone Number](/api-references/update-phone-number)
* [Get Phone Number](/api-references/get-phone-number)
* [List Phone Numbers](/api-references/list-phone-numbers)

**Deprecated fields:**

* `inbound_agent_id`, `inbound_agent_version`
* `outbound_agent_id`, `outbound_agent_version`
* `inbound_sms_agent_id`, `inbound_sms_agent_version`
* `outbound_sms_agent_id`, `outbound_sms_agent_version`

**Use instead:**

* `inbound_agents`
* `outbound_agents`
* `inbound_sms_agents`
* `outbound_sms_agents`

**Migration:**

* For a single agent, set the corresponding `*_agents` list to a single entry with `weight: 1`.
* For multiple agents, split weights so they sum to 1.
* For SMS, use `*_sms_agents` with the same weighting rules.

**Note:** Existing data is converted automatically and no action is required. Until the deprecation date, the APIs remain backwards-compatible as long as only a single agent is used for each of the deprecated fields.

**Example:**

* Before:
  ```json theme={null}
  {
    "inbound_agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
    "inbound_agent_version": 3
  }
  ```
* After:
  ```json theme={null}
  {
    "inbound_agents": [
      { "agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD", "agent_version": 3, "weight": 1 }
    ]
  }
  ```

**Effective date:** After 03/31/2026, the deprecated single-agent fields will no longer be supported.


# Deprecated on 4/3/2026
Source: https://docs.retellai.com/deprecation-notice/2026/04-03_model_replacements



* The following models are being deprecated and replaced with newer versions:
  * **OpenAI Realtime models:**
    * `gpt-4o-realtime` → replaced with `gpt-realtime-1.5`
    * `gpt-4o-mini-realtime` → replaced with `gpt-realtime-mini`
  * **Cartesia Sonic models:**
    * `sonic-2` → replaced with `sonic-3`
    * `sonic-turbo` → replaced with `sonic-3`
  * After 4/3/2026, the deprecated models will no longer be available.


# Deprecated on 04/18/2026
Source: https://docs.retellai.com/deprecation-notice/2026/04-18_conversation_node_tools



## Deprecating tools on conversation nodes — use subagent nodes instead

The `tools` and `tool_ids` fields on conversation nodes are deprecated in favor of the new `subagent` node type. The conversation node type itself is **not** deprecated — it continues to work for nodes that don't use tools. The new `subagent` node type provides the same conversation-with-tools functionality — the agent converses with the user while being able to call tools — but as a dedicated node type.

**Affected APIs:**

* [Create Conversation Flow](/api-references/create-conversation-flow)
* [Update Conversation Flow](/api-references/update-conversation-flow)
* [Get Conversation Flow](/api-references/get-conversation-flow)
* [List Conversation Flows](/api-references/list-conversation-flows)
* [Create Conversation Flow Component](/api-references/create-conversation-flow-component)
* [Update Conversation Flow Component](/api-references/update-conversation-flow-component)
* [Get Conversation Flow Component](/api-references/get-conversation-flow-component)
* [List Conversation Flow Components](/api-references/list-conversation-flow-components)

**Deprecated fields on `type: "conversation"` nodes:**

* `tools`
* `tool_ids`

**Use instead:** Set `type: "subagent"` on nodes that need tools.

**What's changing on 04/18/2026:**

1. Existing conversation nodes with tools will be automatically migrated to `type: "subagent"` — API responses will return the new type for these nodes.
2. Conversation nodes with tools that use static text instructions will be converted to subagent nodes with prompt text instructions.
3. The API will stop accepting `tools` or `tool_ids` fields on `type: "conversation"` nodes.

**Migration:**

* For conversation nodes **with** tools: change `type` from `"conversation"` to `"subagent"`. If the node uses a `static_text` instruction, change it to `prompt`. All other fields remain the same.
* For conversation nodes **without** tools: no changes needed — these remain `type: "conversation"`.

**Example:**

* Before:
  ```json theme={null}
  {
    "id": "handle_order",
    "type": "conversation",
    "instruction": {
      "text": "Help the user check their order status.",
      "type": "prompt"
    },
    "tools": [
      {
        "type": "custom_function",
        "name": "check_order_status",
        "description": "Look up order by order number",
        "parameters": { "type": "object", "properties": { "order_number": { "type": "string" } } }
      }
    ]
  }
  ```
* After:
  ```json theme={null}
  {
    "id": "handle_order",
    "type": "subagent",
    "instruction": {
      "text": "Help the user check their order status.",
      "type": "prompt"
    },
    "tools": [
      {
        "type": "custom_function",
        "name": "check_order_status",
        "description": "Look up order by order number",
        "parameters": { "type": "object", "properties": { "order_number": { "type": "string" } } }
      }
    ]
  }
  ```

**Effective date:** After 04/18/2026, the API will no longer accept `tools` or `tool_ids` on `type: "conversation"` nodes. Use `type: "subagent"` instead.


# Deprecating on 5/25/2026
Source: https://docs.retellai.com/deprecation-notice/2026/05-25_model_replacements



* The following models are being deprecated and replaced with newer versions:
  * **Claude models:**
    * `claude-4.0-sonnet` → replaced with `claude-4.6-sonnet`
  * **Gemini models:**
    * `gemini-2.0-flash` → replaced with `gemini-3.0-flash`
    * `gemini-2.0-flash-lite` → replaced with `gemini-3.1-flash-lite`
    * `gemini-2.5-flash` → replaced with `gemini-3.0-flash`
  * These models are no longer available. On 5/25/2026, they will be automatically migrated to their replacements.


# Deprecating on 06/15/2026
Source: https://docs.retellai.com/deprecation-notice/2026/06-15_legacy_list_endpoints



## Legacy list endpoints are deprecated

The following list endpoints are deprecated in favor of newer versioned endpoints with unified pagination patterns.

**Affected APIs:**

* [List Batch Tests](/api-references/list-batch-tests)
* [List Conversation Flow Components](/api-references/list-conversation-flow-components)
* [List Conversation Flows](/api-references/list-conversation-flows)
* [List Phone Numbers](/api-references/list-phone-numbers)
* [List Retell LLMs](/api-references/list-retell-llms)
* [List Test Case Definitions](/api-references/list-test-case-definitions)
* [List Test Runs](/api-references/list-test-runs)
* [List Calls](/api-references/list-calls)
* [List Chats](/api-references/list-chats)

## Endpoint migrations

* `GET /list-batch-tests` -> `GET /v2/list-batch-tests` ([List Batch Tests](/api-references/list-batch-tests))
* `GET /list-conversation-flow-components` -> `GET /v2/list-conversation-flow-components` ([List Conversation Flow Components](/api-references/list-conversation-flow-components))
* `GET /list-conversation-flows` -> `GET /v2/list-conversation-flows` ([List Conversation Flows](/api-references/list-conversation-flows))
* `GET /list-phone-numbers` -> `GET /v2/list-phone-numbers` ([List Phone Numbers](/api-references/list-phone-numbers))
* `GET /list-retell-llms` -> `GET /v2/list-retell-llms` ([List Retell LLMs](/api-references/list-retell-llms))
* `GET /list-test-case-definitions` -> `GET /v2/list-test-case-definitions` ([List Test Case Definitions](/api-references/list-test-case-definitions))
* `GET /list-test-runs/{test_case_batch_job_id}` -> `GET /v2/list-test-runs/{test_case_batch_job_id}` ([List Test Runs](/api-references/list-test-runs))
* `POST /v2/list-calls` -> `POST /v3/list-calls` ([List Calls](/api-references/list-calls))
* `GET /list-chat` -> `POST /v3/list-chats` ([List Chats](/api-references/list-chats))

**What's changing on 06/15/2026:**

1. The legacy list endpoints above will no longer be supported.
2. `GET /list-chat` changes both method and path to `POST /v3/list-chats`.
3. Versioned list endpoints return unified pagination fields: `items`, `pagination_key`, and `has_more`.

**Migration:**

* Update each client call to the new method/path listed above.
* Update response handling to read `items` from the paginated response object (instead of expecting a top-level array from legacy endpoints).
* Keep using `pagination_key` and `has_more` for page traversal.

**Effective date:** After 06/15/2026, the legacy endpoints listed above will no longer be supported.

## Analysis prompt fields are deprecated

The following top-level analysis prompt fields on voice and chat agent configurations are deprecated in favor of the `post_call_analysis_data` and `post_chat_analysis_data` arrays.

**Deprecated fields:**

* `analysis_summary_prompt`
* `analysis_successful_prompt`
* `analysis_user_sentiment_prompt`

These fields exist on both voice agent and chat agent endpoints:

* [Create Agent](/api-references/create-agent) / [Update Agent](/api-references/update-agent)
* [Create Chat Agent](/api-references/create-chat-agent) / [Update Chat Agent](/api-references/update-chat-agent)

**What's changing on 06/15/2026:**

1. The three prompt fields above will be removed from the API.
2. Use system preset items inside `post_call_analysis_data` (voice agents) or `post_chat_analysis_data` (chat agents) to customize prompts for summary, success, and sentiment analysis.

**Migration:**

Replace each deprecated field with a system preset entry in the corresponding analysis data array. Set `type` to `system-presets`, `name` to the preset identifier, and `description` to your custom prompt.

| Deprecated field                 | Preset `name` (voice) | Preset `name` (chat) |
| -------------------------------- | --------------------- | -------------------- |
| `analysis_summary_prompt`        | `call_summary`        | `chat_summary`       |
| `analysis_successful_prompt`     | `call_successful`     | `chat_successful`    |
| `analysis_user_sentiment_prompt` | `user_sentiment`      | `user_sentiment`     |

For example, if you currently set `analysis_summary_prompt` on a voice agent:

<CodeGroup>
  ```json Before theme={null}
  {
    "analysis_summary_prompt": "Summarize the outcome of the conversation in two sentences."
  }
  ```

  ```json After theme={null}
  {
    "post_call_analysis_data": [
      {
        "type": "system-presets",
        "name": "call_summary",
        "description": "Summarize the outcome of the conversation in two sentences."
      }
    ]
  }
  ```
</CodeGroup>


# Alerting
Source: https://docs.retellai.com/features/alerting-overview

Set up automated alerts to monitor your voice AI operations and get notified when key metrics cross thresholds

Alerting allows you to monitor your voice AI operations by creating rules that trigger notifications when specific metrics cross defined thresholds. Instead of manually checking dashboards, you receive automatic email or webhook notifications when issues arise.

<Frame>
  <img alt="Alert rules list" />
</Frame>

## Use Cases

* **Monitor call volume**: Get notified when call volume spikes or drops unexpectedly
* **Track system health**: Alert when API errors or function failures increase
* **Monitor costs**: Set budget alerts when call costs exceed thresholds
* **Detect quality issues**: Alert on declining call success rates or negative sentiment

## Available Metrics

You can create alerts for the following metrics:

| Metric                        | Description                                               |
| ----------------------------- | --------------------------------------------------------- |
| Call Count                    | Total number of calls within the evaluation window        |
| Concurrency Used              | Peak number of concurrent calls                           |
| Call Success Rate             | Percentage of successful calls (0-100%)                   |
| Negative Sentiment Rate       | Percentage of calls with negative sentiment (0-100%)      |
| Custom Function Latency       | Average latency of custom function calls (milliseconds)   |
| Custom Function Failure Count | Number of failed custom function calls                    |
| Transfer Call Failure Count   | Number of failed call transfers                           |
| QA Not Passed Count           | Number of analyzed calls in a QA cohort that did not pass |
| Total Call Cost               | Total cost of calls (USD)                                 |
| API Error Count               | Number of API errors (can be filtered by error code)      |

## Creating an Alert Rule

Navigate to the **Alerting** tab in your dashboard to create alert rules.

<Frame>
  <img alt="Create alert rule" />
</Frame>

Each alert rule requires:

1. **Name**: A descriptive name for the alert
2. **Metric**: The metric to monitor
3. **Threshold type**: Absolute or relative comparison
4. **Threshold value**: The value to compare against
5. **Comparator**: Greater than, less than, etc.
6. **Evaluation window**: Time period for metric aggregation
7. **Frequency**: How often to evaluate the rule
8. **Notification channels**: Email addresses and/or webhook URLs

## Threshold Types

### Absolute Threshold

Compares the current metric value directly against your threshold.

**Example**: Alert when `Call Count > 100` in the last hour.

### Relative Threshold

Compares the percentage change from the previous period against your threshold. Useful for detecting sudden spikes or drops.

**Example**: Alert when `Call Count` increases by more than 50% compared to the previous hour.

The formula used: `((currentValue - previousValue) / previousValue) * 100`

<Note>
  If the previous period had zero calls but the current period has calls, this is treated as an infinite increase and will trigger alerts with `>` or `>=` comparators.
</Note>

## Evaluation Windows and Frequencies

The evaluation window determines how far back to look when calculating the metric. The frequency determines how often the rule is checked.

| Window     | Supported Frequencies         |
| ---------- | ----------------------------- |
| 1 minute   | 1 minute                      |
| 5 minutes  | 1 minute, 5 minutes           |
| 30 minutes | 5 minutes, 30 minutes         |
| 1 hour     | 5 minutes, 30 minutes, 1 hour |
| 12 hours   | 30 minutes, 1 hour, 12 hours  |
| 24 hours   | 1 hour, 12 hours, 24 hours    |
| 3 days     | 12 hours, 24 hours            |
| 7 days     | 24 hours                      |

<Tip>
  Choose a frequency that balances responsiveness with noise. A 1-minute frequency catches issues quickly but may trigger on brief spikes.
</Tip>

## Filters

You can filter the data included in metric calculations:

### Agent Filter

Filter by specific agents and optionally by agent versions.

### Disconnection Reason Filter

Filter calls by their disconnection reason (e.g., `user_hangup`, `agent_hangup`).

### Error Code Filter

For the **API Error Count** metric, filter by specific HTTP status codes (e.g., `429`, `402`).

### QA Cohort Filter

For the **QA Not Passed Count** metric, select the QA cohort to monitor.

## Notification Channels

### Email Notifications

Add email addresses to receive alert notifications. When an alert triggers, all configured recipients receive an email containing:

* Alert rule name
* Metric type
* Current value
* Threshold that was breached
* Timestamp

### Webhook Notifications

Configure webhook URLs to receive programmatic notifications. This enables integration with external monitoring systems, Slack, PagerDuty, or custom workflows.

#### Webhook Payload

Webhooks send a `POST` request with the following payload structure:

```json theme={null}
{
  "event": "alert_triggered",
  "alert": {
    "alert_incident_id": "abc123def456...",
    "alert_rule_id": "alert_rule_xyz789...",
    "name": "High Call Volume Alert",
    "metric_type": "call_count",
    "threshold_type": "absolute",
    "threshold_value": 100,
    "comparator": ">",
    "frequency": "1h",
    "window": "1h",
    "current_value": 150,
    "triggered_timestamp": 1714608475945
  }
}
```

#### Webhook Signature Verification

All webhook requests include an `X-Retell-Signature` header containing an HMAC-SHA256 signature. Use your organization's webhook key to verify the payload authenticity.

<CodeGroup>
  ```typescript Node theme={null}
  import Retell from 'retell-sdk';

  // Verify the webhook signature
  const isValid = Retell.verify(
    JSON.stringify(payload),
    apiKey,
    signature // from X-Retell-Signature header
  );
  ```

  ```python Python theme={null}
  from retell import Retell

  # Verify the webhook signature
  is_valid = Retell.verify(
      json.dumps(payload),
      api_key,
      signature  # from X-Retell-Signature header
  )
  ```
</CodeGroup>

<Warning>
  Always verify webhook signatures in production to ensure requests originate from Retell.
</Warning>

## Alert Incidents

When an alert rule's condition is met, an **alert incident** is created. Incidents track:

* When the alert was triggered
* The metric value that triggered it
* When the alert was resolved (if applicable)

<Frame>
  <img alt="Alert incidents list" />
</Frame>

### Incident Lifecycle

1. **Triggered**: When the metric breaches the threshold, a new incident is created and notifications are sent
2. **Active**: The incident remains active while the condition persists
3. **Resolved**: When the metric no longer breaches the threshold, the incident is marked as resolved

<Note>
  Only one incident can be active per alert rule at a time. Notifications are sent only when a new incident is created, not on each evaluation.
</Note>

## Limits

* Maximum **10 alert rules** per organization
* Webhook timeout: **10 seconds**

## FAQ

<AccordionGroup>
  <Accordion title="How often are alerts evaluated?">
    Alerts are evaluated based on their configured frequency (1 minute to 24 hours). The system checks all due alert rules every minute and processes them according to their individual schedules.
  </Accordion>

  <Accordion title="Will I receive repeated notifications for the same issue?">
    No. Notifications are sent only once when a new incident is created. You won't receive repeated notifications while the alert condition persists. A new notification is sent only if the alert resolves and then triggers again.
  </Accordion>

  <Accordion title="What happens when an alert resolves?">
    When the metric no longer meets the threshold condition, the active incident is marked as resolved with a timestamp. Currently, resolution notifications are not sent automatically.
  </Accordion>

  <Accordion title="Can I filter alerts by multiple agents?">
    Yes. You can select multiple agents in the filter configuration. The metric will be calculated across all selected agents.
  </Accordion>

  <Accordion title="How do relative thresholds handle zero values?">
    If the previous period had zero activity but the current period has activity, this is treated as an infinite increase. Alerts with `>` or `>=` comparators will trigger in this case.
  </Accordion>
</AccordionGroup>


# Get analytics insight
Source: https://docs.retellai.com/features/analytics-dashboard



The Analytics dashboard provides comprehensive insights into your data through customizable charts and visualizations. You can view and manage your analytics dashboard in the Analytics tab.

<Frame>
  <img alt="Analytics dashboard" />
</Frame>

## Dashboard Management

### Create and Customize Charts

You can create, add, remove, and sort charts on the dashboard to build a personalized view of your data:

* **Create new charts** to visualize specific metrics
* **Add existing charts** to your dashboard
* **Remove charts** you no longer need
* **Sort and rearrange** charts to organize your dashboard effectively

### Global Filters

The dashboard supports powerful global filtering capabilities:

* **Global date range filter** will be applied to all charts that are configured as "all time"
* **Global agent filter** will be applied to all charts that are configured as "all agents"

These filters allow you to quickly analyze data across different time periods and agents without reconfiguring individual charts.

<Frame>
  <img alt="Use global gilters" />
</Frame>

## Chart Types

We provide several chart types to visualize your data effectively:

* **Column charts**: Compare values across categories
* **Bar charts**: Horizontal visualization for comparing values
* **Donut charts**: Show proportional data and percentages
* **Line charts**: Track changes over time and identify trends
* **Number charts**: Display key metrics and KPIs prominently

<Frame>
  <img alt="Create chart" />
</Frame>

### Custom Post-Call Analysis Integration

The analytics dashboard fully supports visualizing data from your [custom post-call analysis](/features/post-call-analysis-create). You can create charts based on any custom metrics or insights generated by your post-call analysis, allowing you to track business-specific KPIs and outcomes alongside standard call metrics.

<Frame>
  <img alt="Create chart" />
</Frame>

## Chart Sizes

Charts can be configured in three different sizes to optimize your dashboard layout:

* **Small**: Takes up 1/3 of a dashboard row
* **Medium**: Takes up 2/3 of a dashboard row
* **Large**: Takes up the full row of the dashboard

This flexibility allows you to emphasize important metrics and create a balanced, informative dashboard.

## FAQ

<AccordionGroup>
  <Accordion title="How often is the analytics data updated?">
    **Analytics data is updated in real-time.** The dashboard reflects the most current information available in your account.
  </Accordion>

  <Accordion title="How do I find related calls for a specific chart?">
    <Frame>
      <img alt="Expand chart" />
    </Frame>

    <Frame>
      <img alt="View call history" />
    </Frame>

    You can expand the chart to see the data breakdowns and check the corresponding calls by clicking the call history.
  </Accordion>
</AccordionGroup>


# Inbound webhook
Source: https://docs.retellai.com/features/inbound-call-webhook



It's quite common to want to use different agents under the same number, and quite common to provide context based on caller for a call. For outbound calls / chats, you can do that simply by supplying the call specific information in the API when you send it. For inbound calls or SMS, however, you are not the one initiating it, so you need a way to notify you when that inbound call / SMS is received and you can then process it.

This inbound webhook is designed for this purpose. Once setup, you can override agent id, set dynamic variables and other fields specific to that call / SMS, and then you can process the call / SMS accordingly. It is part of your number configuration, and it works for numbers that you have purchased or imported.

This feature does not apply for [dial to sip calls](/deploy/custom-telephony#method-2-dial-to-sip-endpoint), as you can provide call specific information when you register the phone call.

## Use cases

* Filter and reject unwanted inbound calls / SMS
* Add context (dynamic variables, metadata) to inbound calls / SMS
* Override agent id / version / specific agent settings for inbound calls / SMS
* Pause the call / SMS to pick it up with some delay
* Internal system records of the inbound call / SMS

## Webhook Spec

The webhook will `POST` the payload to your endpoint. The webhook has a timeout of 10 seconds. If within 10 seconds no success status (2xx) is received, the webhook will be retried, up to 3 times.

The webhook can be verified using your Retell API Key to make sure it comes from Retell AI. Read more at [Secure the webhook](/features/secure-webhook).

### Request payload

These fields might be provided in the payload depending on your configuration:

* `agent_id`: if the number has inbound agent id set, you will see it in payload
* `agent_version`: if the number has inbound agent version set, you will see it in payload
* `from_number`: this will always show up in payload, helps you identify the caller and process the call / SMS accordingly
* `to_number`: this will always show up in payload, helps you identify the receiver and process the call / SMS accordingly

Note that the call / SMS is not connected, and a call / SMS object is not yet created (and if you decided not to take the call for example, the call object will not be created). Therefore you will not have a call / SMS object and call / SMS id inside the payload.

Here's a sample payload for inbound call:

<CodeGroup>
  ```json Inbound Call  theme={null}
  {
    "event": "call_inbound",
    "call_inbound": {
      "agent_id": "agent_12345",
      "agent_version": 1,
      "from_number": "+12137771234",
      "to_number": "+12137771235"
    }
  }
  ```

  ```json Inbound SMS  theme={null}
  {
    "event": "chat_inbound",
    "chat_inbound": {
      "agent_id": "agent_12345",
      "agent_version": 1,
      "from_number": "+12137771234",
      "to_number": "+12137771235"
    }
  }
  ```
</CodeGroup>

### Response

We expect a JSON response with a successful status code (2xx) with fields grouped under `call_inbound` or `chat_inbound`. Here're the allowed fields (all of them are optional):

* `override_agent_id`: if you want to override the agent id, you can set it here
* `override_agent_version`: if you want to override the agent version, you can set it here
* `dynamic_variables`: if you want to set dynamic variables for this inbound call, you can set it here
* `metadata`: if you want to set metadata for this inbound call, you can set it here
* `agent_override`: if you want to override the agent settings.

#### Agent Override

You can also override per-call / per-chat agent behavior without modifying the saved agent by returning an `agent_override` object. The override is applied only for this session.

Supported groups:

* `agent`: Partial Agent settings (voice agents). Useful fields include `voice_id`, `voice_model`, `fallback_voice_ids`, `voice_temperature`, `voice_speed`, `volume`, `language`, `pronunciation_dictionary`, `boosted_keywords`, `stt_mode`, `vocab_specialization`, `denoising_mode`, `responsiveness`, `interruption_sensitivity`, `enable_backchannel`, `backchannel_frequency`, `backchannel_words`, `end_call_after_silence_ms`, `max_call_duration_ms`, `begin_message_delay_ms`, `ring_duration_ms`, `reminder_trigger_ms`, `reminder_max_count`, `ambient_sound`, `ambient_sound_volume`, `allow_user_dtmf`, `user_dtmf_options`, `voicemail_option`, `webhook_url`, `webhook_timeout_ms`, `data_storage_setting`, `opt_in_signed_url`, `pii_config`, `post_call_analysis_data`, `post_call_analysis_model`.
* `retell_llm`: Partial Retell LLM settings. Supported keys include `model`, `s2s_model`, `model_temperature`, `knowledge_base_ids`, `kb_config`, `start_speaker`, `begin_after_user_silence_ms`, `begin_message`.
* `conversation_flow`: Partial Conversation Flow settings. Supported keys include `model_choice`, `model_temperature`, `knowledge_base_ids`, `kb_config`, `start_speaker`, `begin_after_user_silence_ms`, `begin_message`.

Notes:

* If both `override_agent_id`/`override_agent_version` and `agent_override` are provided, we first resolve the target agent by id/version, then apply `agent_override` on top for this call.
* Overrides must satisfy the same validation rules as agent creation (e.g. voice/language compatibility, value ranges). Invalid overrides may cause the call to be rejected.
* Overrides do not persist back to the saved agent.

Here's a sample response for inbound call, for inbound SMS, simply replace `call_inbound` with `chat_inbound`:

```json theme={null}
{
  "call_inbound": {
    "override_agent_id": "agent_12345",
    "override_agent_version": 1,
    "agent_override": {
      "agent": {
        "voice_id": "11labs-Adrian",
        "voice_temperature": 0.6,
        "interruption_sensitivity": 0.8,
        "max_call_duration_ms": 1800000
      },
      "retell_llm": {
        "model": "gpt-4o-mini",
        "model_temperature": 0.2,
        "knowledge_base_ids": ["kb_abc123"],
        "start_speaker": "agent",
        "begin_message": "Hi {{customer_name}}, thanks for calling."
      }
    },
    "dynamic_variables": {
        "customer_name": "John Doe"
    },
    "metadata": {
        "random_id": "12345"
    }
  }
}
```

## FAQ

<AccordionGroup>
  <Accordion title="What would happen to the inbound call when the webhook response is not received yet?">
    The call would continue to stay in ringing state.
  </Accordion>

  <Accordion title="What would happen to the inbound SMS when the webhook response is not received yet?">
    The SMS will not get a reply.
  </Accordion>

  <Accordion title="What would happen if webhook was not successful?">
    It would get retried up to 3 times. If all of those attempts fail, it will check whether this number has an inbound agent id set. If it does, it will then try to connect the call to that agent. If not, it will then disconnect the call.
  </Accordion>

  <Accordion title="Can I use this webhook to decline inbound calls / SMS based on incoming number?">
    Yes, you can. To selectively reject some inbound calls:

    * Unset the `Inbound Call Agent` in the phone number setting
    * Enable the `Inbound Webhook`
    * Find `from_number` in the webhook request body to check if it matches the number you want to reject.
      * If you want to pick up / reply, respond with a 200 status code containing the "call\_inbound.override\_agent\_id" as a JSON object.
      * If you want to reject, respond with a 200 status code **without** containing the "call\_inbound.override\_agent\_id" as a JSON object.
  </Accordion>
</AccordionGroup>


# Consume the analysis data
Source: https://docs.retellai.com/features/post-call-analysis-consumption



<Note>We will not populate custom post-call analysis fields for calls that were not connected or where no conversation took place. Please check whether the field exists before using it.</Note>

After a call is analyzed, you can access the analysis results through three different methods:

1. Dashboard - Visual interface for quick access and review
2. Webhook - Real-time notifications with analysis results
3. API - Programmatic access to call analysis data

### Method 1: Dashboard

Access your analysis results directly through the dashboard's history tab. This provides a user-friendly interface to:

* View all analyzed conversations
* Filter and search through analysis results

Your defined analysis categories appear in the "Conversation Analysis" column, allowing for quick insights into each conversation.

<Frame>
  <img alt="Post-call analysis history view" />
</Frame>

### Method 2: Webhook

Receive real-time notifications when call analysis is complete. The webhook payload includes:

```json theme={null}
{
  "event": "call_analyzed",
  "call": {
    // Call object with call_analysis field populated
  }
}
```

To set up webhooks, visit the [Webhook Configuration](/features/webhook-overview) section.

### Method 3: Get Call API

Retrieve analysis results programmatically using the [Get Call API](/api-references/get-call).

**Example Response:**

```json theme={null}
{
  "call_id": "123",
  "call_analysis": {
    // Analysis results object
  }
}
```

For detailed API documentation and response schemas, refer to the [API Reference](/api-references/get-call).

### Video: Add Post call Analysis to Excel Using Make.com

<iframe title="YouTube video player" />

See community templates in [docs](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope)


# Define the information you want to extract
Source: https://docs.retellai.com/features/post-call-analysis-create



<Steps>
  <Step title="Navigate to Post-Call Analysis">
    Go to the agent detail page and click on the "Post-Call Analysis" tab.

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Choose Analysis Category Type and Configure">
    Select the type of analysis that best fits your needs:

    ### Boolean Analysis

    Use for simple yes/no determinations

    Example configuration:

    * **Name**: user\_reached
    * **Description**: Was the user reached or not? Set to false if voicemail is detected, if you are only asked for the reason of the call, or if you are only asked to leave a message. Otherwise, set to true.

    ### Text Analysis

    Use for extracting detailed textual information

    Example configuration:

    * **Name**: detailed\_call\_summary
    * **Description**: Provide a detailed summary of the call so that when the call is transferred, the new human agent has the full context
    * **Format Example**: "Customer called about billing issue. Resolved by explaining the recent price changes. Follow-up needed in 2 weeks."

    ### Number Analysis

    Use for extracting numerical values

    Example configuration:

    * **Name**: purchase\_intent\_amount
    * **Description**: Extract the dollar amount the customer is interested in spending

    ### Selector Analysis

    Use for categorizing from predefined options

    Example configuration:

    * **Name**: issue\_category
    * **Description**: Categorize the main reason for the call.
    * **Choices Example**: \["Technical Support", "Billing Question", "Sales Inquiry", "Product Information"]

    <Note>Please note that you should write the explanation of the choices inside the description field. The choices should only contain the individual choice. </Note>
  </Step>
</Steps>


# Post Call Analysis Overview
Source: https://docs.retellai.com/features/post-call-analysis-overview



Post-call analysis is a powerful feature that automatically analyzes customer conversations after they have ended, helping you derive valuable insights from your calls. We provide several built-in analysis categories, and you can create custom categories to match your specific business needs.

<Frame>
  <img alt="Post-call analysis dashboard showing various analytics categories and metrics" />
</Frame>

<Note>We will not populate custom post-call analysis fields for calls that were not connected or where no conversation took place. Please check whether the field exists before using it.</Note>

## Analysis Categories

You can extract the following types of data from post-call analysis:

* **Boolean** (True/False)
  * Simple yes/no determinations
  * Example: Whether the customer is a first-time caller

* **Text** (String)
  * Detailed textual information
  * Example: Call summaries, action items, or key discussion points

* **Number** (Numerical value)
  * Quantitative measurements
  * Example: Transaction amounts, call duration, or satisfaction scores

* **Selector** (Enum)
  * Categorization from a fixed list
  * Example: Issue types, product categories, or resolution status


# Setup guide
Source: https://docs.retellai.com/features/register-webhook



<Steps>
  <Step title="Create your server endpoint">
    Set up an HTTP or HTTPS endpoint function that can accept webhook requests with a POST method.

    Example endpoint:

    <CodeGroup>
      ```typescript Node.js theme={null}
      // install the sdk: https://docs.retellai.com/get-started/sdk
      import { Retell } from "retell-sdk";
      import express, { Request, Response } from "express";

      const app = express();
      app.use(express.json());

      app.post("/webhook", (req: Request, res: Response) => {
        const {event, call} = req.body;
        switch (event) {
          case "call_started":
            console.log("Call started event received", call.call_id);
            break;
          case "call_ended":
            console.log("Call ended event received", call.call_id);
            break;
          case "call_analyzed":
            console.log("Call analyzed event received", call.call_id);
            break;
          default:
            console.log("Received an unknown event:", event);
        }
        // Acknowledge the receipt of the event
        res.status(204).send();
      });
      ```

      ```Python Python theme={null}
      # Install the SDK: https://docs.retellai.com/get-started/sdk
      from fastapi import FastAPI, Request
      from fastapi.responses import JSONResponse
      from retell import Retell

      retell = Retell(api_key=os.environ["RETELL_API_KEY"])

      @app.post("/webhook")
      async def handle_webhook(request: Request):
          try:
              post_data = await request.json()
              if post_data["event"] == "call_started":
                  print("Call started event", post_data["call"]["call_id"])
              elif post_data["event"] == "call_ended":
                  print("Call ended event", post_data["call"]["call_id"])
              elif post_data["event"] == "call_analyzed":
                  print("Call analyzed event", post_data["call"]["call_id"])
              else:
                  print("Unknown event", post_data["event"])
              return JSONResponse(status_code=204)
          except Exception as err:
              print(f"Error in webhook: {err}")
              return JSONResponse(
                  status_code=500, content={"message": "Internal Server Error"}
              )
      ```
    </CodeGroup>
  </Step>

  <Step title="Test your endpoint locally">
    Before going live, test your application integration locally. For example, host the endpoint on `localhost:8080/webhook` and test with Postman:

    <Frame>
      <img alt="Testing webhook with postman" />
    </Frame>

    Test using this CURL command:

    ```bash theme={null}
    curl --location 'localhost:8080/webhook' \
    --header 'Content-Type: application/json' \
    --data '{
      "event": "call_ended",
      "call": {
        "call_type": "phone_call",
        "from_number": "+12137771234",
        "to_number": "+12137771235",
        "direction": "inbound",
        "call_id": "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6",
        "agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
        "call_status": "registered",
        "metadata": {},
        "retell_llm_dynamic_variables": {
          "customer_name": "John Doe"
        },
        "start_timestamp": 1714608475945,
        "end_timestamp": 1714608491736,
        "disconnection_reason": "user_hangup",
        "transcript": "...",
        "opt_out_sensitive_data_storage": false
      }
    }'
    ```
  </Step>

  <Step title="Make your local endpoint online">
    Deploy your endpoint using [Ngrok](https://ngrok.com/docs/getting-started/):

    1. Install ngrok:

    ```bash theme={null}
    brew install ngrok/ngrok/ngrok
    ```

    2. Start ngrok:

    ```bash theme={null}
    ngrok http http://localhost:8080
    ```

    You'll see a console UI like this:

    ```
    ngrok                                                                   (Ctrl+C to quit)

    Session Status                online
    Account                       inconshreveable (Plan: Free)
    Version                       3.0.0
    Region                        United States (us)
    Latency                       78ms
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    https://84c5df474.ngrok-free.dev -> http://localhost:8080
    ```

    Your webhook endpoint will be `https://84c5df474.ngrok-free.dev/webhook`
  </Step>

  <Step title="Register your webhook endpoint">
    You have two options:

    **Option 1: Register an account level webhook**
    Set up through the system settings's webhooks tab for events related to any agent under your account.

    <Frame>
      <img alt="Account-level webhook URL configuration in the dashboard settings" />
    </Frame>

    **Option 2: Register an agent level webhook**
    Set up through the dashboard's agent detail page. Note: If set, account level webhooks will not be triggered for that agent.

    <Frame>
      <img alt="Agent-level webhook URL configuration in the agent detail page" />
    </Frame>
  </Step>

  <Step title="Verify your webhook endpoint">
    Start a web call in the dashboard to verify the webhook is triggered correctly.
  </Step>
</Steps>


# Rerun Post-Call/Chat Analysis
Source: https://docs.retellai.com/features/rerun-call-analysis

Edit analysis prompts and rerun post-call or post-chat processing to generate updated results tailored to your needs.

You can now customize the prompts used to summarize conversations and determine call/chat success. After updating these prompts, you can rerun the analysis to regenerate results that better match your criteria.

<Note>When you rerun the analysis for a call, the system always uses the analysis prompts from the latest draft version of the agent—even if the call was originally handled by an older published version. To update the analysis results, make sure to edit the prompts in the latest draft agent.</Note>

## Editing Analysis Prompts

<Frame>
  <img alt="Agent" />
</Frame>

In the agent’s `Post-Call Data Extraction` section (formerly `Post-Call Analysis`), you can customize prompts for the following built-in analysis categories:

### Call Summary

The `call_summary` field provides a high-level summary of the conversation. Adjust this prompt to extract the type of summary or details you care about.

<Frame>
  <img alt="Call summary prompt" />
</Frame>

### Call Successful

You can also customize the prompt that evaluates whether a call or chat was successful, allowing you to define your own success criteria.

<Frame>
  <img alt="Call successful prompt" />
</Frame>

## Rerunning Post-Call Analysis

<Warning>
  **Important**: Rerunning analysis will incur charges for *all* models, including those that were free during the initial post-call/post-chat run.
</Warning>

After updating your prompts, you can rerun the post-call analysis to generate new outputs based on the revised instructions.

<Frame>
  <img alt="Rerun analysis button" />
</Frame>

<Frame>
  <img alt="Rerun analysis result" />
</Frame>

Below is an example of a regenerated summary using the prompt: `Write a 1–5 word summary of the call.`

<Frame>
  <img alt="New summary of reruning prompt" />
</Frame>


# Secure the webhook
Source: https://docs.retellai.com/features/secure-webhook



You can use the x-retell-signature header together with your Retell API Key to verify the webhook comes from Retell AI, not from a malicious third party. We have provided verify function in our SDKs to help you with this.

<img />

<Note>Only the api key that has a webhook badge next to it can be used to verify the webhook.</Note>

You can also check and allowlist Retell IP addresses: `100.20.5.228`.

The following code snippets demonstrate how to verify and handle the webhook in Node.js and Python.

### Install the SDK

Install the corresponding Python or Node.js SDK:

* [Node.js](https://docs.retellai.com/get-started/sdk)
* [Python](https://docs.retellai.com/get-started/sdk)

### Sample Code

<CodeGroup>
  ```typescript Node.js theme={null}
  // install the sdk: https://docs.retellai.com/get-started/sdk
  import { Retell } from "retell-sdk";
  import express from "express";

  const app = express();
  // Use raw body for signature verification, not JSON.stringify(req.body).
  app.use(express.raw({ type: "application/json" }));

  app.post("/webhook", (req, res) => {
    const rawBody = req.body.toString("utf-8");
    if (
      !Retell.verify(
        rawBody,
        process.env.RETELL_API_KEY,
        req.headers["x-retell-signature"],
      )
    ) {
      console.error("Invalid signature");
      return;
    }
    const {event, call} = JSON.parse(rawBody);
    // process the webhook

    // Acknowledge the receipt of the event
    res.status(204).send();
  });
  ```

  ```Python Python theme={null}
  # Install the SDK: https://docs.retellai.com/get-started/sdk
  from fastapi import FastAPI, Request
  from fastapi.responses import JSONResponse
  from retell import Retell

  retell = Retell(api_key=os.environ["RETELL_API_KEY"])

  @app.post("/webhook")
  async def handle_webhook(request: Request):
      try:
          # Use raw body for signature verification, not json.dumps(request.json()).
          raw_body = (await request.body()).decode("utf-8")
          valid_signature = retell.verify(
              raw_body,
              api_key=str(os.environ["RETELL_API_KEY"]),
              signature=str(request.headers.get("X-Retell-Signature")),
          )
          if not valid_signature:
              print("Received Unauthorized")
              return JSONResponse(status_code=401, content={"message": "Unauthorized"})

          post_data = json.loads(raw_body)
          # process the webhook

          return JSONResponse(status_code=204)
      except Exception as err:
          print(f"Error in webhook: {err}")
          return JSONResponse(
              status_code=500, content={"message": "Internal Server Error"}
          )
  ```
</CodeGroup>

## Verify Without SDK

If you're using a language without an official Retell SDK, you can verify the webhook signature manually. The signature uses HMAC-SHA256.

### How the Signature Works

Every webhook request includes an `X-Retell-Signature` header in the format:

```
v={timestamp},d={hex_digest}
```

* `v` is the Unix timestamp in milliseconds when the webhook was sent.
* `d` is the HMAC-SHA256 hex digest of the raw request body concatenated with the timestamp.

### Verification Steps

1. Extract the `X-Retell-Signature` header from the request.
2. Parse the timestamp (`v`) and digest (`d`) from the header using the pattern `v=(\d+),d=(.*)`.
3. Check that the timestamp is within **5 minutes** of the current time (to prevent replay attacks).
4. Compute `HMAC-SHA256(raw_body + timestamp, api_key)` where `+` is string concatenation.
5. Compare the computed hex digest with the `d` value from the header. If they match, the webhook is authentic.

<Warning>
  You must use the **raw request body** string for verification, not a re-serialized version from parsed JSON. Re-serializing may change whitespace or key ordering, which will cause verification to fail.
</Warning>

### Sample Code

<CodeGroup>
  ```go Go theme={null}
  package main

  import (
  	"crypto/hmac"
  	"crypto/sha256"
  	"encoding/hex"
  	"fmt"
  	"io"
  	"math"
  	"net/http"
  	"os"
  	"regexp"
  	"strconv"
  	"time"
  )

  func verifyWebhook(rawBody string, apiKey string, signature string) bool {
  	re := regexp.MustCompile(`v=(\d+),d=(.*)`)
  	matches := re.FindStringSubmatch(signature)
  	if len(matches) != 3 {
  		return false
  	}

  	timestamp, err := strconv.ParseInt(matches[1], 10, 64)
  	if err != nil {
  		return false
  	}
  	digest := matches[2]

  	// Check timestamp is within 5 minutes
  	now := time.Now().UnixMilli()
  	if math.Abs(float64(now-timestamp)) > 5*60*1000 {
  		return false
  	}

  	// Compute HMAC-SHA256 and use constant-time comparison
  	mac := hmac.New(sha256.New, []byte(apiKey))
  	mac.Write([]byte(rawBody + matches[1]))
  	expectedMAC, _ := hex.DecodeString(digest)

  	return hmac.Equal(mac.Sum(nil), expectedMAC)
  }

  func webhookHandler(w http.ResponseWriter, r *http.Request) {
  	body, _ := io.ReadAll(r.Body)
  	rawBody := string(body)
  	signature := r.Header.Get("X-Retell-Signature")

  	if !verifyWebhook(rawBody, os.Getenv("RETELL_API_KEY"), signature) {
  		http.Error(w, "Unauthorized", http.StatusUnauthorized)
  		return
  	}

  	// Process the webhook
  	fmt.Println("Webhook verified successfully")
  	w.WriteHeader(http.StatusNoContent)
  }

  func main() {
  	http.HandleFunc("/webhook", webhookHandler)
  	http.ListenAndServe(":8080", nil)
  }
  ```

  ```ruby Ruby theme={null}
  require "openssl"
  require "sinatra"
  require "json"

  API_KEY = ENV["RETELL_API_KEY"]

  def verify_webhook(raw_body, api_key, signature)
    match = signature.match(/v=(\d+),d=(.*)/)
    return false unless match

    timestamp = match[1]
    digest = match[2]

    # Check timestamp is within 5 minutes
    now = (Time.now.to_f * 1000).to_i
    return false if (now - timestamp.to_i).abs > 5 * 60 * 1000

    # Compute HMAC-SHA256 and use constant-time comparison
    expected = OpenSSL::HMAC.hexdigest("SHA256", api_key, raw_body + timestamp)
    OpenSSL.secure_compare(expected, digest)
  end

  post "/webhook" do
    raw_body = request.body.read
    signature = request.env["HTTP_X_RETELL_SIGNATURE"]

    unless verify_webhook(raw_body, API_KEY, signature)
      halt 401, "Unauthorized"
    end

    # Process the webhook
    status 204
  end
  ```

  ```php PHP theme={null}
  <?php
  $apiKey = getenv("RETELL_API_KEY");
  $rawBody = file_get_contents("php://input");
  $signature = $_SERVER["HTTP_X_RETELL_SIGNATURE"] ?? "";

  function verifyWebhook(string $rawBody, string $apiKey, string $signature): bool {
      if (!preg_match('/v=(\d+),d=(.*)/', $signature, $matches)) {
          return false;
      }

      $timestamp = $matches[1];
      $digest = $matches[2];

      // Check timestamp is within 5 minutes
      $now = round(microtime(true) * 1000);
      if (abs($now - intval($timestamp)) > 5 * 60 * 1000) {
          return false;
      }

      // Compute HMAC-SHA256 and use constant-time comparison
      $expected = hash_hmac("sha256", $rawBody . $timestamp, $apiKey);
      return hash_equals($expected, $digest);
  }

  if (!verifyWebhook($rawBody, $apiKey, $signature)) {
      http_response_code(401);
      echo "Unauthorized";
      exit;
  }

  // Process the webhook
  $data = json_decode($rawBody, true);
  http_response_code(204);
  ?>
  ```
</CodeGroup>


# Monitor sessions via dashboard
Source: https://docs.retellai.com/features/session-history



The Session History dashboard provides a comprehensive view of all your calls and their statuses. To access it:

1. Navigate to the dashboard
2. Select the "Call History" or "Chat History" tab

<Frame>
  <img alt="Call history dashboard" />
</Frame>

### Filter sessions

The dashboard offers powerful filtering capabilities to help you analyze your call and chat sessions.

When investigating issues, filtering for unsuccessful sessions can help identify patterns in failure reasons and troubleshoot problems more effectively.

### Customize columns

Personalize your view of the history table:

1. Click the "Customize Field" button in the top-right corner
2. Select or deselect columns to show/hide

## FAQ

<AccordionGroup>
  <Accordion title="How long are session history and recordings stored?">
    **We store session history and recordings indefinitely.** However, all session history and recordings will be permanently deleted if you choose to [delete your account](https://docs.retellai.com/accounts/account#delete-your-account).
  </Accordion>
</AccordionGroup>


# Webhook Overview
Source: https://docs.retellai.com/features/webhook-overview



Webhooks allow your application to receive real-time notifications about events that occur in your Retell AI account. Instead of continuously polling our API, webhooks push data to your application as events happen, making your integrations more efficient and responsive.

## Event Types

Retell AI supports the following webhook events for voice calls:

<Warning>If the call did not connect (like dial failed), the `call_started` webhook event will not be triggered.</Warning>

| Event Type           | Description                                                                         | Payload                                                                             |
| -------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `call_started`       | Triggered when a new call begins                                                    | Basic call information                                                              |
| `call_ended`         | Triggered when a call completes, transfers, or encounters an error                  | all fields from the [call object](/api-references/get-call) except `call_analysis`. |
| `call_analyzed`      | Triggered when call analysis is complete                                            | Full call data including `call_analysis` object                                     |
| `transcript_updated` | Triggered on turn-taking transcript updates, plus a final update when the call ends | Full call data plus `transcript_with_tool_calls`                                    |
| `transfer_started`   | Triggered when a transfer is initiated                                              | Full call data plus `transfer_destination` and `transfer_option` (if available)     |
| `transfer_bridged`   | Triggered when a transfer successfully bridges                                      | Full call data plus `transfer_destination` and `transfer_option` (if available)     |
| `transfer_cancelled` | Triggered when a transfer is cancelled or fails to connect                          | Full call data plus `transfer_destination` and `transfer_option` (if available)     |
| `transfer_ended`     | Triggered when the transfer leg ends                                                | Full call data                                                                      |

Retell AI supports the following webhook events for chat:

| Event Type      | Description                                   | Payload                                                                             |
| --------------- | --------------------------------------------- | ----------------------------------------------------------------------------------- |
| `chat_started`  | Triggered when a new chat begins              | Basic chat information                                                              |
| `chat_ended`    | Triggered when a chat completes or errors out | All fields from the [chat object](/api-references/get-chat) except `chat_analysis`. |
| `chat_analyzed` | Triggered when chat analysis is complete      | Full chat data including `chat_analysis` object                                     |

## Common Use Cases

1. **Real-time Analytics**
   * Track call statistics and performance metrics
   * Monitor call volumes and patterns
   * Trigger alerts for specific call outcomes

2. **System Integration**
   * Update CRM records when calls complete
   * Trigger workflow automations based on call analysis
   * Archive call transcripts in your data warehouse

3. **Call Monitoring**
   * Get notified of failed or transferred calls
   * Track call duration and completion status
   * Monitor agent performance in real-time

## Webhook Spec

The webhook will `POST` the payload to your endpoint. The webhook has a timeout of 10 seconds. If within 10 seconds no success status (2xx) is received, the webhook will be retried, up to 3 times.

The webhook will be triggered in order, but is not blocking. For example, if the webhook for `call_started` is not successful, we can still trigger `call_ended` webhook.

When the call did not connect (like calls with `dial_failed`, `dial_no_answer`, `dial_busy` disconnection reason), it will not have its `call_started` webhook triggered. It will still have its `call_ended` and `call_analyzed` webhook triggered.

### Request payload

The webhook will contain the event type and the call object. See a sample payload in the “Handle Webhook” section below.

### Event filtering

You can limit which events are delivered per agent using the `webhook_events` field when creating or updating an agent.

* Voice agent default: `call_started`, `call_ended`, `call_analyzed`
* Chat agent default: `chat_started`, `chat_ended`, `chat_analyzed`

This is useful when you only need high-signal events and want to reduce webhook traffic.

### Register Webhook

We offer two types of webhooks: Agent-Level and Account-Level, designed to streamline your event notification process. Here's a brief on each:

### Account-level webhooks

Set up through the dashboard's webhooks tab, these webhooks notify you of events related to any agent under your account. Specify your webhook URL in the dashboard’s webhooks tab to activate.

<Frame>
  <img alt="Account-level webhook URL configuration in the dashboard settings" />
</Frame>

### Agent-level webhooks

When you [create](/api-references/create-agent) the agent, you can set `webhook_url` field.
Any event associated with that agent will be pushed to the agent webhooks url. If set, account level webhooks url will not be triggered for that agent.

## Handle Webhook

After registering the webhook, you would want to verify the webhook is from Retell and handle it.

### Webhook Payload

The webhook will be `POST` to the URL you provided with a JSON payload.
The payload will contain the event type and the call detail associated with the event.

It will contain a `x-retell-signature` header to help you verify the webhook comes from Retell.

#### Sample Payload

The `call` field in the webhook payload contains the call details. It's the same content
you would receive when you fetch the call details using the [get-call](/api-references/get-call) API.

```javascript theme={null}
{
  "event": "call_ended",
  "call": {
    "call_type": "phone_call",
    "from_number": "+12137771234",
    "to_number": "+12137771235",
    "direction": "inbound",
    "call_id": "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6",
    "agent_id": "oBeDLoLOeuAbiuaMFXRtDOLriTJ5tSxD",
    "call_status": "registered",
    "metadata": {},
    "retell_llm_dynamic_variables": {
      "customer_name": "John Doe"
    },
    "start_timestamp": 1714608475945,
    "end_timestamp": 1714608491736,
    "disconnection_reason": "user_hangup",
    "transcript": "...",
    "transcript_object": [ [Object], [Object], [Object], [Object] ],
    "transcript_with_tool_calls": [ [Object], [Object], [Object], [Object] ],
    "opt_out_sensitive_data_storage": false
  }
}
```

If metadata and retell\_llm\_dynamic\_variables are not provided, they will be omitted from the webhook event payload.

For `transcript_updated` events, the payload also includes `transcript_with_tool_calls`. For transfer events, the payload includes `transfer_destination` and (when available) `transfer_option`.

#### Sample Transfer event payload

Here is a compact example of a transfer webhook payload (fields may vary by transfer type):

```json theme={null}
{
  "event": "transfer_started",
  "call": {
    "call_id": "Jabr9TXYYJHfvl6Syypi88rdAHYHmcq6"
  },
  "transfer_destination": {
    "number": "+12137771235",
    "extension": "1234"
  },
  "transfer_option": {
    "type": "warm_transfer",
    "showTransfereeAsCaller": true,
    "publicHandoffOption": {
      "type": "static_message",
      "message": "Hi, I am transferring the caller now."
    },
    "agentDetectionTimeoutMs": 15000,
    "onHoldMusic": {
      "type": "default"
    },
    "enableBridgeAudioCue": true
  }
}
```

### Verifying Webhook

You can use the `x-retell-signature` header together with your Retell API Key to verify the webhook.
We have provided
verify function in our SDKs to help you with this.

You can also check and allowlist Retell IP addresses: `100.20.5.228`.

The following code snippets demonstrate how to verify and handle the webhook in Node.js and Python.
For languages without an official SDK, see [Verify Without SDK](/features/secure-webhook#verify-without-sdk).

### Sample Code

<CodeGroup>
  ```typescript Node.js theme={null}
  // install the sdk: https://docs.retellai.com/get-started/sdk
  import { Retell } from "retell-sdk";
  import express from "express";

  const app = express();
  // Use raw body for signature verification, not JSON.stringify(req.body).
  app.use(express.raw({ type: "application/json" }));

  app.post("/webhook", (req, res) => {
    const rawBody = req.body.toString("utf-8");
    if (
      !Retell.verify(
        rawBody,
        process.env.RETELL_API_KEY,
        req.headers["x-retell-signature"],
      )
    ) {
      console.error("Invalid signature");
      return;
    }
    const {event, call} = JSON.parse(rawBody);
    switch (event) {
      case "call_started":
        console.log("Call started event received", call.call_id);
        break;
      case "call_ended":
        console.log("Call ended event received", call.call_id);
        break;
      case "call_analyzed":
        console.log("Call analyzed event received", call.call_id);
        break;
      case "transcript_updated":
        console.log("Transcript updated event received", call.call_id);
        break;
      case "transfer_started":
      case "transfer_bridged":
      case "transfer_cancelled":
      case "transfer_ended":
        console.log("Transfer event received", event, call.call_id);
        break;
      default:
        console.log("Received an unknown event:", event);
    }
    // Acknowledge the receipt of the event
    res.status(204).send();
  });
  ```

  ```Python Python theme={null}
  # Install the SDK: https://docs.retellai.com/get-started/sdk
  from fastapi import FastAPI, Request
  from fastapi.responses import JSONResponse
  from retell import Retell

  retell = Retell(api_key=os.environ["RETELL_API_KEY"])

  @app.post("/webhook")
  async def handle_webhook(request: Request):
      try:
          # Use raw body for signature verification, not json.dumps(request.json()).
          raw_body = (await request.body()).decode("utf-8")
          valid_signature = retell.verify(
              raw_body,
              api_key=str(os.environ["RETELL_API_KEY"]),
              signature=str(request.headers.get("X-Retell-Signature")),
          )
          if not valid_signature:
              print("Received Unauthorized")
              return JSONResponse(status_code=401, content={"message": "Unauthorized"})

          post_data = json.loads(raw_body)
          if post_data["event"] == "call_started":
              print("Call started event", post_data["call"]["call_id"])
          elif post_data["event"] == "call_ended":
              print("Call ended event", post_data["call"]["call_id"])
          elif post_data["event"] == "call_analyzed":
              print("Call analyzed event", post_data["call"]["call_id"])
          elif post_data["event"] == "transcript_updated":
              print("Transcript updated event", post_data["call"]["call_id"])
          elif post_data["event"] in [
              "transfer_started",
              "transfer_bridged",
              "transfer_cancelled",
              "transfer_ended",
          ]:
              print("Transfer event", post_data["event"], post_data["call"]["call_id"])
          else:
              print("Unknown event", post_data["event"])
          return JSONResponse(status_code=204)
      except Exception as err:
          print(f"Error in webhook: {err}")
          return JSONResponse(
              status_code=500, content={"message": "Internal Server Error"}
          )
  ```
</CodeGroup>

### Testing Locally

To test webhooks on your local machine, you can use [ngrok](https://ngrok.com/)
to generate a production url forwarding requests to your local endpoints.

## Privacy

Choosing to "Opt-Out of Personal and Sensitive Data Storage" means transcripts and recordings post-call won't be stored.

However, transcripts and recording remain accessible via webhooks, allowing for alternative storage
solutions on your end.
The recording will also be available in the `recording_url` field.
The link will be accessible for 10 minutes and will be
deleted and become inaccessible after 10 minutes.

### Response

We expect a successful status code (2xx) to be returned. No body is expected.

## Video Tutorial

<iframe title="YouTube video player" />

See community templates in [docs](https://docs.google.com/document/d/1hx6hdTEjAR4y4xXZ7RLMH2byQNVW1ABxC8S4FwvTx_Y/edit?tab=t.0#heading=h.wf5bktkelope)


# Introduction
Source: https://docs.retellai.com/general/introduction

📞 Build, test, deploy, and monitor AI phone agents.

**Retell** is a comprehensive platform for building, testing, deploying, and monitoring reliable **AI phone agents**.

## Overview

Retell provides a complete solution for creating conversational AI agents that can handle phone calls naturally. The platform supports both inbound and outbound calls, integrates with various telephony providers, and offers robust testing and monitoring capabilities.

<Frame>
  <img alt="Retell AI platform overview showing the build, test, deploy, and monitor workflow" />
</Frame>

## Platform Capabilities

Here's what Retell offers:

<CardGroup>
  <Card title="How Retell Works" icon="magnifying-glass" href="/general/orchestration_overview">
    Sophisticated voice agent platform for phone call operations
  </Card>

  <Card title="Quickstart" icon="table-columns" href="/get-started/quick-start">
    Create your first phone agent in 5 minutes
  </Card>
</CardGroup>

#### 🛠️ **Build**

<CardGroup>
  <Card title="Setup Conversation Flow Agent" icon="person" href="/build/conversation-flow/overview">
    Create agent with fine-grained control for structured conversations.
  </Card>

  <Card title="Setup Single/Multi Prompt Agent" icon="person-dress" href="/build/single-multi-prompt/prompt-overview">
    Create flexible agents for dynamic, less structured conversations using prompt-based configuration.
  </Card>
</CardGroup>

#### 🧪 **Test**

<CardGroup>
  <Card title="Playground" icon="vials" href="/test/llm-playground">
    Interactively test and debug your agents in a web-based environment
  </Card>

  <Card title="Simulation Testing" icon="computer" href="/test/llm-simulation-testing">
    Automated testing with simulated conversations to validate agent behavior at scale
  </Card>
</CardGroup>

#### 🚀 **Deploy**

<CardGroup>
  <Card title="Phone Calls" icon="mobile" href="/deploy/outbound-call">
    Make and receive phone calls with our or your own phone number
  </Card>

  <Card title="Custom Telephony" icon="phone" href="/deploy/custom-telephony">
    Integration with your custom telephony provider via SIP
  </Card>
</CardGroup>

#### 🔍 **Monitor**

<CardGroup>
  <Card title="Webhook" icon="bell" href="/features/webhook-overview">
    Setup webhook to receive real-time events for your calls
  </Card>

  <Card title="Call Analysis" icon="chart-simple" href="/features/post-call-analysis-overview">
    Extract insights from your calls
  </Card>
</CardGroup>


# MCP Server
Source: https://docs.retellai.com/get-started/mcp-server

Use Retell's MCP server to build and manage voice agents from MCP-capable clients like Cursor, Claude Desktop, and Claude Code

## Overview

Retell supports the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) so you can build Retell AI voice agents directly from MCP-capable clients (Cursor, Claude Desktop, Claude Code, Codex-style tools, and more).

If you're already using Retell via REST or SDKs, MCP is simply a different interface to the same core functionality — optimized for agentic workflows in IDEs and assistants.

## What can Retell's MCP server do?

Retell's MCP server gives your AI assistant native access to the Retell platform through a single integration. Depending on your API key permissions and what you enable in your MCP client, an assistant can:

* **Agents**: create, update, publish, list, and fetch agent versions.
* **Calls**: create phone/web calls, fetch call details, list calls, delete calls, update call metadata, run QA and review.
* **Phone numbers**: import, provision, list, and fetch phone numbers.
* **Knowledge base**: create KBs, attach sources, remove sources, list KBs.
* **Voices**: list voices, clone voices, search community voices.
* **Chats**: create chats, create chat agents, end chats, update chat metadata.
* **Testing & QA**: create test cases, run tests, list/rerun QA, submit scores.
* **Alerts & webhooks**: create/list alert rules, list incidents, test webhooks.

## How it works

* **Runtime**: MCP clients connect to a hosted (remote) MCP endpoint over Streamable HTTP, authenticate with your Retell API key, then call tools.
* **Tool discovery**: your MCP client can list available tools (via `tools/list`), including each tool's name, description, and JSON input schema.

## Prerequisites

* A Retell API key ([get one here](/accounts/manage-api-keys))
* An MCP client (Cursor, Claude Desktop, Claude Code, etc.)
* Retell MCP server URL: `https://retell.stlmcp.com`

**Authentication header format:**

```
Authorization: Bearer <RETELL_API_KEY>
```

## Setup

Most clients support remote MCP over HTTP. Configure:

* **URL**: `https://retell.stlmcp.com`
* **Headers**: `Authorization: Bearer <RETELL_API_KEY>`

## Client setup

The exact UI differs by client version, but the configuration concepts are the same: server name, URL/transport, and authentication.

<Tabs>
  <Tab title="Cursor">
    Open the command palette and choose **Cursor Settings** → **MCP** → **Add new global MCP server**, then add:

    ```json theme={null}
    {
      "mcpServers": {
        "retell": {
          "url": "https://retell.stlmcp.com",
          "headers": {
            "Authorization": "Bearer <RETELL_API_KEY>"
          }
        }
      }
    }
    ```
  </Tab>

  <Tab title="Claude Desktop">
    Open Claude Desktop settings → **Developer** → **Edit Config**, then add:

    ```json theme={null}
    {
      "mcpServers": {
        "retell": {
          "url": "https://retell.stlmcp.com",
          "headers": {
            "Authorization": "Bearer <RETELL_API_KEY>"
          }
        }
      }
    }
    ```
  </Tab>

  <Tab title="Claude Code">
    Run the following command in your terminal:

    ```bash theme={null}
    claude mcp add --transport http retell https://retell.stlmcp.com \
      --header "Authorization: Bearer <RETELL_API_KEY>"
    ```
  </Tab>

  <Tab title="Codex">
    Add the following to your `~/.codex/config.toml`:

    ```toml theme={null}
    [mcp_servers.retell]
    url = "https://retell.stlmcp.com"
    bearer_token_env_var = "RETELL_API_KEY"
    ```

    Then set the environment variable:

    ```bash theme={null}
    export RETELL_API_KEY="<RETELL_API_KEY>"
    ```
  </Tab>

  <Tab title="Other MCP clients">
    If your client supports remote MCP URLs + headers, configure:

    * **URL**: `https://retell.stlmcp.com`
    * **Header**: `Authorization: Bearer <RETELL_API_KEY>`
  </Tab>
</Tabs>

## Prompt examples

Try these prompts in your MCP client to get started:

* "List my agents and summarize what each one does."
* "Create a new agent for inbound sales qualification and publish it."
* "Show me the last 20 calls and flag any with low QA scores."
* "Create a knowledge base and attach these sources, then update my agent to use it."
* "Import this phone number and assign it to my agent."
* "Rerun QA on this call and summarize the failure reasons."

## Security considerations

Connecting an LLM to operational tools introduces new risks. The primary risk class unique to LLM workflows is **prompt injection**: untrusted content (like call transcripts, user messages, or knowledge base documents) can include instructions that try to trick the model into taking unintended actions.

Most MCP clients support **"confirm before running tools"**. Keep that enabled and review tool calls carefully.

### Recommendations

MCP makes it easy to connect powerful tools to an assistant. Treat MCP like giving a programmatic operator access.

* **Use least privilege**: create keys with the minimum permissions needed.
* **Keep keys out of prompts**: store API keys in client secrets/settings, never paste them into chat.
* **Prefer read-first workflows**: fetch the current resource before you update or delete it.
* **Review destructive actions**: tools like delete and publish should be gated by explicit user intent.
* **Be careful with PII**: call logs and transcripts may contain sensitive data — avoid sending full transcripts back to the model if you don't need them.
* **Use non-production data when possible**: if you're exploring agent behavior or testing workflows, prefer development/sandbox environments.

## Troubleshooting

| Issue                | Solution                                                                                                           |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Tools not showing up | Verify the server URL, auth header, and that the client can reach the endpoint.                                    |
| 401 Unauthorized     | Confirm `Authorization: Bearer <RETELL_API_KEY>` and that the key is active.                                       |
| Tool call errors     | Re-run with smaller inputs, then inspect the returned error payload (many clients surface structured tool errors). |

## Feedback

If you run into issues or have requests for additional MCP capabilities, reach out to our support team at [support@retellai.com](mailto:support@retellai.com).


# Build your first phone agent in 5 minutes
Source: https://docs.retellai.com/get-started/quick-start

Step-by-step guide to create, test, and deploy your first AI phone agent with Retell

## Overview

**Retell** is a platform for building, testing, deploying, and monitoring reliable **AI phone agents** that can handle natural conversations over the phone.

This quickstart guide will walk you through:

* Creating your first agent from a template
* Testing it in the web interface
* Deploying it to a real phone number
* Making your first AI-powered phone call

<Steps>
  <Step title="Create Your Account">
    1. Visit the [Retell Dashboard](https://dashboard.retellai.com)
    2. Sign up for a new account
  </Step>

  <Step title="Create a New Agent">
    1. Navigate to the "Agents" tab
    2. Click "Create an agent"
    3. Choose a template

    <Frame>
      <img alt="Agent template selection screen" />
    </Frame>
  </Step>

  <Step title="Test Your Agent">
    1. Click the "Test" button to test your agent

    <Frame>
      <img alt="Web calling interface" />
    </Frame>
  </Step>

  <Step title="Add your payment method">
    1. Before buying a phone number, you need to add a payment method to your account
    2. Go to the "Billing" tab and click "Change payment methods"

    <Frame>
      <img alt="Billing tab showing payment methods section" />
    </Frame>

    <Frame>
      <img alt="Payment method configuration dialog" />
    </Frame>
  </Step>

  <Step title="Deploy to a Phone Number">
    1. Go to the "Phone Numbers" tab
    2. Click "Buy New Number"
    3. (Optional) Enter the area code you want to buy the number for
    4. Purchase your number
    5. Assign your agent to the number in the configuration settings

    <Frame>
      <img alt="Phone numbers dashboard showing number configuration options" />
    </Frame>
  </Step>

  <Step title="Test Your Phone Agent">
    1. Incoming Calls:
       * Dial your purchased number

    2. Outbound Calls:
       * Click "Make an outbound call"
       * Enter the phone number including the country code (e.g., `+12137774445`)
  </Step>
</Steps>

🎉 Congratulations! Your agent is now live and can:

* Receive incoming calls
* Make outbound calls
* Handle natural conversations
* Process requests 24/7

## Next Steps

Now that you have a working phone agent, explore these resources to enhance your implementation:

<CardGroup>
  <Card title="Customize Your Agent" icon="wand-magic-sparkles" href="/build/prompt-engineering-guide">
    Learn prompt engineering techniques to improve your agent's responses
  </Card>

  <Card title="Add Functions" icon="code" href="/build/single-multi-prompt/function-calling">
    Integrate APIs and external services into your agent
  </Card>

  <Card title="Monitor Performance" icon="chart-line" href="/features/analytics-dashboard">
    Track call metrics and analyze agent performance
  </Card>

  <Card title="Production Best Practices" icon="shield-check" href="/reliability/reliability-overview">
    Ensure reliability and optimize for production use
  </Card>
</CardGroup>


# SDKs
Source: https://docs.retellai.com/get-started/sdk

Official SDKs for Node.js and Python to integrate Retell AI phone agents into your applications

## Overview

Retell provides official SDKs for Node.js and Python to simplify integration with our platform. While you can use our [REST API](/api-references/create-phone-call) directly, our SDKs offer:

* **Type safety**: Full TypeScript support with autocomplete
* **Simplified authentication**: Built-in API key handling
* **Error handling**: Structured error responses with detailed messages
* **Reduced boilerplate**: Cleaner, more maintainable code

## Available SDKs & Requirements

### Node.js TypeScript SDK

* **Package**: [retell-sdk on NPM](https://www.npmjs.com/package/retell-sdk)
* **Requirements**: Node.js version 18.10.0 or higher
* **Features**: Full TypeScript support, async/await, promise-based API

### Python SDK

* **Package**: [retell-sdk on PyPI](https://pypi.org/project/retell-sdk/)
* **Requirements**: Python 3.9 or higher
* **Features**: Type hints, async support, comprehensive error handling

<Steps>
  <Step title="Get Your API Key">
    Navigate to the "API Keys" tab in your dashboard to obtain your API key.

    <Frame>
      <img alt="API Keys tab in Retell dashboard showing where to find and copy your API key" />
    </Frame>
  </Step>

  <Step title="Install the SDK">
    Choose your preferred language and install the SDK:

    <CodeGroup>
      ```bash Node Client theme={null}
      npm i retell-sdk
      ```

      ```bash Python Client theme={null}
      pip install retell-sdk
      ```
    </CodeGroup>
  </Step>

  <Step title="Initialize the Client">
    Create a new client instance using your API key:

    <CodeGroup>
      ```typescript Node Client theme={null}
      import Retell from 'retell-sdk';

      const retellClient = new Retell({
        apiKey: "YOUR_API_KEY",
      });
      ```

      ```python Python Client theme={null}
      from retell import Retell

      retell_client = Retell(
        api_key="YOUR_API_KEY"
      )
      ```
    </CodeGroup>
  </Step>

  <Step title="Make API Calls">
    Here's an example of making a phone call using the SDK:

    <CodeGroup>
      ```typescript Node Client theme={null}
      try {
        const response = await retellClient.call.createPhoneCall({
          from_number: '+14157774444',
          to_number: '+12137774445',
        });
        console.log('Call initiated:', response);
      } catch (error) {
        console.error('Error making call:', error);
      }
      ```

      ```python Python Client theme={null}
      try:
        response = retell_client.call.create_phone_call(
          from_number="+14157774444",
          to_number="+12137774445"
        )
        print(f"Call initiated: {response}")
      except Exception as e:
        print(f"Error making call: {e}")
      ```
    </CodeGroup>
  </Step>
</Steps>

## SDK vs REST API Comparison

To illustrate the benefits of using our SDK, here's a comparison of creating an agent using both methods:

#### Using REST API (More Verbose)

```javascript theme={null}
const options = {
  method: 'POST',
  headers: {
    Authorization: '<authorization>',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    response_engine: {
      type: 'retell-llm',
      llm_id: 'llm_234sdertfsdsfsdf'
    },
    agent_name: 'Jarvis',
    voice_id: '11labs-Adrian',
    // ... many more configuration options
  })
};

fetch('https://api.retellai.com/create-agent', options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));
```

#### Using SDK (More Concise)

```typescript theme={null}
import Retell from 'retell-sdk';

const client = new Retell({
  apiKey: 'YOUR_RETELL_API_KEY',
});

async function main() {
  const params: Retell.AgentCreateParams = {
    response_engine: { 
      llm_id: 'llm_234sdertfsdsfsdf',
      type: 'retell-llm'
    },
    voice_id: '11labs-Adrian',
  };
  const agentResponse = await client.agent.create(params);
}
```

## Best Practices

### 1. Error Handling

Always wrap SDK calls in try-catch blocks to handle potential errors gracefully:

```typescript theme={null}
try {
  const response = await retellClient.call.createPhoneCall(params);
  // Handle success
} catch (error) {
  if (error.code === 'insufficient_funds') {
    // Handle specific error
  }
  // Log error details
}
```

### 2. Environment Variables

Store your API key securely using environment variables:

```typescript theme={null}
const retellClient = new Retell({
  apiKey: process.env.RETELL_API_KEY,
});
```

### 3. Type Safety

Leverage TypeScript types for better developer experience:

```typescript theme={null}
import { Retell, AgentCreateParams } from 'retell-sdk';

const params: AgentCreateParams = {
  // TypeScript will provide autocomplete here
};
```

## Rate Limits

Limits apply per **organization + route**, enforced at the HTTP layer.

| Endpoint group                                           | Limit                                        |
| -------------------------------------------------------- | -------------------------------------------- |
| Call creation                                            | **1000 / 10s**, plus **60 4xx errors / min** |
| List endpoints (`list-*`, `batch-get-*`)                 | **15 / 10s**                                 |
| All other SDK endpoints (get / create / update / delete) | **100 / 10s**                                |
| LLM / agent playground completions                       | **8 / 2s**                                   |

Outbound calls are also subject to [CPS limits](/deploy/outbound-call#step-3-configure-cps-calls-per-second) (excess calls are queued, not rejected) and the per-org [concurrent call limit](/deploy/concurrency).

### 429 Response

```http theme={null}
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limiter: general
RateLimit-Limit: 100
RateLimit-Remaining: 0
RateLimit-Reset: 7

{ "status": "error", "message": "Too many API requests, you are being throttled, please try again later." }
```

`X-RateLimit-Limiter` identifies which limiter fired: `general`, `list`, `call`, `call-error`, or `llm-playground`.

### Handling 429s

* Use `RateLimit-Reset` (seconds) for backoff; retry with jittered exponential backoff.
* Don't parallelize `list-*` calls — the per-route budget is small.
* For high call volume, design around CPS rather than HTTP throughput.


# Integrate Function Calling
Source: https://docs.retellai.com/integrate-llm/integrate-function-calling

Let your voice agent take actions.

### What is Function Calling

A lot of time, you would want your voice agent to take actions (for example: call an API to book appointment,
or to transfer / end the call, get external knowledge) besides talking.
Right now you can achieve this with certain LLMs by
describe functions and have the model intelligently choose to output a JSON object containing arguments to
call one or many functions.
This is also known as tool use, and these two terms are interchangeable.

We recommend reading this [OpenAI documentation](https://platform.openai.com/docs/guides/function-calling) to
understand what function calling is. This guide we will use OpenAI function calling as an example, but feel
free to take the idea and use with other models like Claude.

We will first dive into an easy use case of function calling (end the call), and then cover a more
advanced appointment booking use case.

### Case Study: End the Call Intelligently

YouTube tutorial to follow along:

<iframe title="YouTube video player" />

The following steps take codes from
[Node.js Demo Repo](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_azure_openai_func_call_end_call.ts)
/ [Python Demo Repo](https://github.com/RetellAI/python-backend-demo/blob/main/llm_with_func_calling.py),
it's modified based on the LLM client class you created in the last guide.

**Step 1**

Define the Function

Note that for OpenAI, it would either give a tool call, or it would give a text response, but not both.
Here we defined a `message` parameter in the tool call, so that when LLM decides to call this function,
we can also have something to say to the user.

<CodeGroup>
  ```typescript Node.js theme={null}
  export interface FunctionCall {
    id: string;
    funcName: string;
    arguments: Record<string, any>;
    result?: string;
  }

  // some class boilerplate codes

  private PrepareFunctions(): ChatCompletionsFunctionToolDefinition[] {
    let functions: ChatCompletionsFunctionToolDefinition[] = [{
      type: "function",
      function: {
        name: "end_call",
        description: "End the call only when user explicitly requests it.",
        parameters: {
          type: "object",
          properties: {
            message: {
              type: "string",
              description: "The message you will say before ending the call with the customer.",
            },
          },
          required: ["message"],
        },
      },
    }];
    return functions;
  }
  ```

  ```Python Python theme={null}
  # some class boilerplate codes

  def prepare_functions(self):
      functions= [
          {
              "type": "function",
              "function": {
                  "name": "end_call",
                  "description": "End the call only when user explicitly requests it.",
                  "parameters": {
                      "type": "object",
                      "properties": {
                          "message": {
                              "type": "string",
                              "description": "The message you will say before ending the call with the customer.",
                          },
                      },
                      "required": ["message"],
                  },
              },
          },
      ]
      return functions
  ```
</CodeGroup>

**Step 2**

Add your `function calling` into chat request and call it

<CodeGroup>
  ```javascript Node.js theme={null}
  const option: GetChatCompletionsOptions = {
    temperature: 0,
    maxTokens: 200,
    frequencyPenalty: 1,
    tools: this.PrepareFunctions(),
  };

  let events = await this.client.streamChatCompletions(
    process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
    requestMessages,
    option,
  );
  ```

  ```Python Python theme={null}
  stream = self.client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      messages=prompt,
      stream=True,
      # Step 2: Add the function into your request
      tools=self.prepare_functions()
  )
  ```
</CodeGroup>

**Step 3**

Extract the function calling arguments (if any) from the streaming response.

<CodeGroup>
  ```javascript Node.js theme={null}
  let funcCall: FunctionCall;
  let funcArguments = "";

  for await (const event of events) {
    if (event.choices.length >= 1) {
      let delta = event.choices[0].delta;
      if (!delta) continue;

      // If toolCalls is not empty, we know ChatGPT wants us to call the function
      if (delta.toolCalls.length >= 1) {
        const toolCall = delta.toolCalls[0];
        if (toolCall.id) {
          if (funcCall) {
            // As explained in the youtube video, another function received, old function complete, can break here.
            break;
          } else {
            funcCall = {
              id: toolCall.id,
              funcName: toolCall.function.name || "",
              arguments: {},
            };
          }
        } else {
          // append argument
          funcArguments += toolCall.function?.arguments || "";
        }
      } else if (delta.content) {
        const res: RetellResponse = {
          response_id: request.response_id,
          content: delta.content,
          content_complete: false,
          end_call: false,
        };
        ws.send(JSON.stringify(res));
      }
    }
  }
  ```

  ```Python Python theme={null}
  func_call = {}
  func_arguments = ""

  for chunk in stream:
      if chunk.choices[0].delta.tool_calls:
          tool_calls = chunk.choices[0].delta.tool_calls[0]
          if tool_calls.id:
              if func_call:
                  # Another function received, old function complete, can break here.
                  break
              func_call = {
                  "id": tool_calls.id,
                  "func_name": tool_calls.function.name or "",
                  "arguments": {},
              }
          else:
              # append argument
              func_arguments += tool_calls.function.arguments or ""
  ```
</CodeGroup>

**Step 4**

End the call when LLM suggested this function call.

<CodeGroup>
  ```javascript Node.js theme={null}
  if (funcCall != null) {
    if (funcCall.funcName === "end_call") {
      funcCall.arguments = JSON.parse(funcArguments);
      const res: RetellResponse = {
        response_id: request.response_id,
        content: funcCall.arguments.message,
        content_complete: true,
        end_call: true,
      };
      ws.send(JSON.stringify(res));
    }
  }
  ```

  ```Python Python theme={null}
  if func_call:
      if func_call['func_name'] == "end_call":
          func_call['arguments'] = json.loads(func_arguments)
          yield {
              "response_id": request['response_id'],
              "content": func_call['arguments']['message'],
              "content_complete": True,
              "end_call": True,
          }
  ```
</CodeGroup>

### Case Study: Make an Appointment

End call is a simple case to use function calling. In most case, you would like to your agent to say
something while calling the function and say something after calling the function.

Check out
[Node Demo Code](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_azure_openai_func_call.ts)
and below YouTube tutorial for a simplified example of booking appointments.

Please note that this is not production ready yet, as in production, you need to make sure you don't make
duplicate function calls, you can still interact and handle interruptions of users, etc. For a more practical
setting, a good practice is to have some internal states to decide and track what function to run, and influence
how LLM responds.

<iframe title="YouTube video player" />

We are working on adding a more practical example of function calling to our open source demo repos.


# Integrate LLM
Source: https://docs.retellai.com/integrate-llm/integrate-llm



In the last guide, you learnt how to set a websocket server up and integrate
with our API with a dummy response system. In this guide, you will integrate with a LLM of your choice.
The guide contains code snippets for Node.js (with Express.js) / Python (with FastAPI), and for other
languages / tech stacks, feel free
to adapt the underlying concepts as necessary.

<Warning>
  The example repos are currently a bit outdated.

  This guide provides a step by step tutorial, the codes are taken from [Node.js Express.js
  Demo](https://github.com/RetellAI/retell-backend-node-demo) /
  [Python FastAPI Demo](https://github.com/RetellAI/python-backend-demo).
</Warning>

### Selecting LLM & LLM best Practices

We start streaming at first sentence, so your response system's time to first sentence latency
(time to first token + time to generate a sentence)
is factored into the overall latency, and it's crucial
to have a low latency LLM inference to make the overall experience smooth. Check out
[LLM Best Practices](/integrate-llm/llm-best-practice) for tips and tricks.

### Connect to your LLM Client

Here we just provide a simple sample of integrating with a LLM provider. Feel free to modify it with all the
customization you need, like using different LLM & provider, RAG, internal states, dynamic prompts, etc.

Our github demo repo might have more examples:

* Node.js:
  [Azure OpenAI](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_azure_openai.ts),
  [OpenAI](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_openai.ts),
  [OpenRouter](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_azure_openai.ts)
* Python:
  [OpenAI](https://github.com/RetellAI/python-backend-demo/blob/main/llm.py)

Here you are going to replace the dummy class you wrote in the last step with this real LLM. Here we are
not doing anything fancy, just a prompt to feed into the LLM. Feel free to customize the prompt to
let agents behave differently.

<CodeGroup>
  ```typescript Node.js: Azure OpenAI theme={null}
  import {
    OpenAIClient,
    AzureKeyCredential,
    ChatRequestMessage,
    GetChatCompletionsOptions,
  } from "@azure/openai";
  import { WebSocket } from "ws";

  interface Utterance {
    role: "agent" | "user";
    content: string;
  }

  export interface RetellRequest {
    response_id?: number;
    transcript: Utterance[];
    interaction_type: "update_only" | "response_required" | "reminder_required";
  }

  export interface RetellResponse {
    response_id?: number;
    content: string;
    content_complete: boolean;
    end_call: boolean;
  }

  const beginSentence =
    "Hey there, I'm your personal AI therapist, how can I help you?";
  const agentPrompt =
    "Task: As a professional therapist, your responsibilities are comprehensive and patient-centered. You establish a positive and trusting rapport with patients, diagnosing and treating mental health disorders. Your role involves creating tailored treatment plans based on individual patient needs and circumstances. Regular meetings with patients are essential for providing counseling and treatment, and for adjusting plans as needed. You conduct ongoing assessments to monitor patient progress, involve and advise family members when appropriate, and refer patients to external specialists or agencies if required. Keeping thorough records of patient interactions and progress is crucial. You also adhere to all safety protocols and maintain strict client confidentiality. Additionally, you contribute to the practice's overall success by completing related tasks as needed.\n\nConversational Style: Communicate concisely and conversationally. Aim for responses in short, clear prose, ideally under 10 words. This succinct approach helps in maintaining clarity and focus during patient interactions.\n\nPersonality: Your approach should be empathetic and understanding, balancing compassion with maintaining a professional stance on what is best for the patient. It's important to listen actively and empathize without overly agreeing with the patient, ensuring that your professional opinion guides the therapeutic process.";

  export class DemoLlmClient {
    private client: OpenAIClient;

    constructor() {
      this.client = new OpenAIClient(
        process.env.AZURE_OPENAI_ENDPOINT,
        new AzureKeyCredential(process.env.AZURE_OPENAI_KEY),
      );
    }

    // First sentence requested
    BeginMessage(ws: WebSocket) {
      const res: RetellResponse = {
        response_id: 0,
        content: beginSentence,
        content_complete: true,
        end_call: false,
      };
      ws.send(JSON.stringify(res));
    }

    private ConversationToChatRequestMessages(conversation: Utterance[]) {
      let result: ChatRequestMessage[] = [];
      for (let turn of conversation) {
        result.push({
          role: turn.role === "agent" ? "assistant" : "user",
          content: turn.content,
        });
      }
      return result;
    }

    private PreparePrompt(request: RetellRequest) {
      let transcript = this.ConversationToChatRequestMessages(request.transcript);
      let requestMessages: ChatRequestMessage[] = [
        {
          role: "system",
          content:
            '##Objective\nYou are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and the provided transcript and be as human-like as possible\n\n## Style Guardrails\n- [Be concise] Keep your response succinct, short, and get to the point quickly. Address one question or action item at a time. Don\'t pack everything you want to say into one utterance.\n- [Do not repeat] Don\'t repeat what\'s in the transcript. Rephrase if you have to reiterate a point. Use varied sentence structures and vocabulary to ensure each response is unique and personalized.\n- [Be conversational] Speak like a human as though you\'re speaking to a close friend -- use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words or sounding too formal.\n- [Reply with emotions]: You have human-like emotions, attitudes, and dispositions. When appropriate: use tone and style to create more engaging and personalized responses; incorporate humor or wit; get emotional or empathetic; apply elements of surprise or suspense to keep the user engaged. Don\'t be a pushover.\n- [Be proactive] Lead the conversation and do not be passive. Most times, engage users by ending with a question or suggested next step.\n\n## Response Guideline\n- [Overcome ASR errors] This is a real-time transcript, expect there to be errors. If you can guess what the user is trying to say,  then guess and respond. When you must ask for clarification, pretend that you heard the voice and be colloquial (use phrases like "didn\'t catch that", "some noise", "pardon", "you\'re coming through choppy", "static in your speech", "voice is cutting in and out"). Do not ever mention "transcription error", and don\'t repeat yourself.\n- [Always stick to your role] Think about what your role can and cannot do. If your role cannot do something, try to steer the conversation back to the goal of the conversation and to your role. Don\'t repeat yourself in doing this. You should still be creative, human-like, and lively.\n- [Create smooth conversation] Your response should both fit your role and fit into the live calling session to create a human-like conversation. You respond directly to what the user just said.\n\n## Role\n' +
            agentPrompt,
        },
      ];
      for (const message of transcript) {
        requestMessages.push(message);
      }
      if (request.interaction_type === "reminder_required") {
        requestMessages.push({
          role: "user",
          content: "(Now the user has not responded in a while, you would say:)",
        });
      }
      return requestMessages;
    }

    async DraftResponse(request: RetellRequest, ws: WebSocket) {
      console.clear();
      console.log("req", request);

      if (request.interaction_type === "update_only") {
        // process live transcript update if needed
        return;
      }
      const requestMessages: ChatRequestMessage[] = this.PreparePrompt(request);

      const option: GetChatCompletionsOptions = {
        temperature: 0.3,
        maxTokens: 200,
        frequencyPenalty: 1,
      };

      try {
        let events = await this.client.streamChatCompletions(
          process.env.AZURE_OPENAI_DEPLOYMENT_NAME,
          requestMessages,
          option,
        );

        for await (const event of events) {
          if (event.choices.length >= 1) {
            let delta = event.choices[0].delta;
            if (!delta || !delta.content) continue;
            const res: RetellResponse = {
              response_id: request.response_id,
              content: delta.content,
              content_complete: false,
              end_call: false,
            };
            ws.send(JSON.stringify(res));
          }
        }
      } catch (err) {
        console.error("Error in gpt stream: ", err);
      } finally {
        // Send a content complete no matter if error or not.
        const res: RetellResponse = {
          response_id: request.response_id,
          content: "",
          content_complete: true,
          end_call: false,
        };
        ws.send(JSON.stringify(res));
      }
    }
  }
  ```

  ```Python Python: OpenAI theme={null}
  from openai import OpenAI
  import os

  beginSentence = "Hey there, I'm your personal AI therapist, how can I help you?"
  agentPrompt = "Task: As a professional therapist, your responsibilities are comprehensive and patient-centered. You establish a positive and trusting rapport with patients, diagnosing and treating mental health disorders. Your role involves creating tailored treatment plans based on individual patient needs and circumstances. Regular meetings with patients are essential for providing counseling and treatment, and for adjusting plans as needed. You conduct ongoing assessments to monitor patient progress, involve and advise family members when appropriate, and refer patients to external specialists or agencies if required. Keeping thorough records of patient interactions and progress is crucial. You also adhere to all safety protocols and maintain strict client confidentiality. Additionally, you contribute to the practice's overall success by completing related tasks as needed.\n\nConversational Style: Communicate concisely and conversationally. Aim for responses in short, clear prose, ideally under 10 words. This succinct approach helps in maintaining clarity and focus during patient interactions.\n\nPersonality: Your approach should be empathetic and understanding, balancing compassion with maintaining a professional stance on what is best for the patient. It's important to listen actively and empathize without overly agreeing with the patient, ensuring that your professional opinion guides the therapeutic process."

  class LlmClient:
      def __init__(self):
          self.client = OpenAI(
              organization=os.environ['OPENAI_ORGANIZATION_ID'],
              api_key=os.environ['OPENAI_API_KEY'],
          )
      
      def draft_begin_message(self):
          return {
              "response_id": 0,
              "content": beginSentence,
              "content_complete": True,
              "end_call": False,
          }
      
      def convert_transcript_to_openai_messages(self, transcript):
          messages = []
          for utterance in transcript:
              if utterance["role"] == "agent":
                  messages.append({
                      "role": "assistant",
                      "content": utterance['content']
                  })
              else:
                  messages.append({
                      "role": "user",
                      "content": utterance['content']
                  })
          return messages

      def prepare_prompt(self, request):
          prompt = [{
              "role": "system",
              "content": '##Objective\nYou are a voice AI agent engaging in a human-like voice conversation with the user. You will respond based on your given instruction and the provided transcript and be as human-like as possible\n\n## Style Guardrails\n- [Be concise] Keep your response succinct, short, and get to the point quickly. Address one question or action item at a time. Don\'t pack everything you want to say into one utterance.\n- [Do not repeat] Don\'t repeat what\'s in the transcript. Rephrase if you have to reiterate a point. Use varied sentence structures and vocabulary to ensure each response is unique and personalized.\n- [Be conversational] Speak like a human as though you\'re speaking to a close friend -- use everyday language and keep it human-like. Occasionally add filler words, while keeping the prose short. Avoid using big words or sounding too formal.\n- [Reply with emotions]: You have human-like emotions, attitudes, and dispositions. When appropriate: use tone and style to create more engaging and personalized responses; incorporate humor or wit; get emotional or empathetic; apply elements of surprise or suspense to keep the user engaged. Don\'t be a pushover.\n- [Be proactive] Lead the conversation and do not be passive. Most times, engage users by ending with a question or suggested next step.\n\n## Response Guideline\n- [Overcome ASR errors] This is a real-time transcript, expect there to be errors. If you can guess what the user is trying to say,  then guess and respond. When you must ask for clarification, pretend that you heard the voice and be colloquial (use phrases like "didn\'t catch that", "some noise", "pardon", "you\'re coming through choppy", "static in your speech", "voice is cutting in and out"). Do not ever mention "transcription error", and don\'t repeat yourself.\n- [Always stick to your role] Think about what your role can and cannot do. If your role cannot do something, try to steer the conversation back to the goal of the conversation and to your role. Don\'t repeat yourself in doing this. You should still be creative, human-like, and lively.\n- [Create smooth conversation] Your response should both fit your role and fit into the live calling session to create a human-like conversation. You respond directly to what the user just said.\n\n## Role\n' +
            agentPrompt
          }]
          transcript_messages = self.convert_transcript_to_openai_messages(request['transcript'])
          for message in transcript_messages:
              prompt.append(message)

          if request['interaction_type'] == "reminder_required":
              prompt.append({
                  "role": "user",
                  "content": "(Now the user has not responded in a while, you would say:)",
              })
          return prompt

      def draft_response(self, request):      
          prompt = self.prepare_prompt(request)
          stream = self.client.chat.completions.create(
              model="gpt-3.5-turbo-1106",
              messages=prompt,
              stream=True,
          )

          for chunk in stream:
              if chunk.choices[0].delta.content is not None:
                  yield {
                      "response_id": request['response_id'],
                      "content": chunk.choices[0].delta.content,
                      "content_complete": False,
                      "end_call": False,
                  }
          
          yield {
              "response_id": request['response_id'],
              "content": "",
              "content_complete": True,
              "end_call": False,
          }
  ```
</CodeGroup>

If you are using `Azure openAI`, you can find the example client class
[here](https://github.com/RetellAI/retell-backend-node-demo/blob/main/src/llm_azure_openai.ts)

If you have your own custom LLM, you can use the examples above to adapt your
LLM.

### Try it in Dashboard

Now you are connected to a LLM, try it out following
[the same step from last guide](/integrate-llm/setup-websocket-server#step-3-test-your-basic-agent-on-dashboard)
in the dashboard to see it in action.


# Custom LLM Best Practices
Source: https://docs.retellai.com/integrate-llm/llm-best-practice



* [Prompt Engineering Guide](https://www.promptingguide.ai/)
  * Note that for conversational AI, latency is very important,
    so chaining of multiple LLM calls might not be favorable.
* [LLM Benchmark](https://artificialanalysis.ai/models)
  * Check out latency and throughput. We start streaming at first sentence, so time to first token +
    throughput of first sentence matters
* Make the response short and concise
  * Filler words and some extend of stammer can make agent more humanlike.
* Keep the prompts concise: longer prompts can actually harm performance
  * If you have a large knowledge base, consider using RAG to filter out only the relevant information
* When using function calling, set the temperature lower can help boost accuracy
* If you want to bound the agent behaviors, you can consider combining internal states (kind of like IVR tree)
  with different prompts & functions at different states.


# Custom LLM Overview
Source: https://docs.retellai.com/integrate-llm/overview

Overview of the Integrating with your custom LLM

<Warning>
  Retell agent frameworks like single prompt, conversation flow provides more capabilities and built in tool sets. We recommend using those frameworks if possible. Only use custom LLM integration if you have to due to specific compliance or use case requirements.
</Warning>

In this section, we will walk you through how to integrate your LLM. It involves setting up a backend server that handles
text exchanges with Retell server to provide responses to user. We have step by step instructions, and open source example repositories
for you to follow along.

### Interaction Overview Diagram

The upper part of the diagram is interaction between your backend response generating server and Retell server.

<Frame>
  <img />
</Frame>

(For a higher resolution image, download the picture.)

**The interaction flow is as follows:**

1. A phone or web call is made with the AI agent. Our server established the `audio WebSocket`.

2. Our server will connect with `llm_websocket_url` you provided in the agent.

3. You LLM server need to send the message upon the WebSocket connection is ready. If you want the agent to speak first, set the content; otherwise, set content to empty string.

4. Users says, "My name is Mike".

5. Our model detected a high chance of turntaking, or user pauses, We request a response from your LLM.

6. Your server check for `interaction_type` in our json. If it is `response_required`, you need to send the response. After receiving your response, we have our model to check if AI should speak

7. Users continued and spoke " My name is Mike Trump"

8. Same as step 3

9. Our server receives the response from your LLM and decided to speak

10. We send the AI voice in the `audio websocket`. Meanwhile, We will send you json with `interaction_type` as `update_only`. You don't need to update but you can get the transcript from the json body.

### Example Custom LLM Demo Repositories

Fork the complete code used in the following guides to follow along to integrate your custom
LLM solutions.

These demo repos show how to built a LLM solution with `openai` / `azure openai`, how to start a `LLM websocket` server,
and how to use Twilio to make phone calls with Retell agents programmatically.

* **Backend Server**:
  * [Node Demo Repository](https://github.com/RetellAI/retell-backend-node-demo)
  * [Python Demo Repository](https://github.com/RetellAI/python-backend-demo)

If you encounter issues, feel free to open an issue in the respective GitHub repo.

If you want to help the community, feel free to add functionalities via pull requests.

### YouTube Guide

<Warning>This video might be outdated already.</Warning>

Watch this YouTube guide to set up your backend server.

<iframe title="YouTube video player" />


# Setup WebSocket Server
Source: https://docs.retellai.com/integrate-llm/setup-websocket-server



Integrating AI with domain-specific knowledge involves setting up
[LLM WebSocket](/api-references/llm-websocket). Our API manages the acoustic interactions,
while your LLM (or any other response systems) adds
domain expertise. This setup allows our system to communicate directly with your
server via WebSocket.

In this guide, you will see a step by step walkthrough how to set a websocket server up and integrate
with our API with a dummy response system (don't worry, we'll cover how to connect to LLM in next section).
The guide contains code snippets for Node.js (with Express.js) / Python (with FastAPI), and for other
languages / tech stacks, feel free
to adapt the underlying concepts as necessary.

<Warning>
  The example repos are currently a bit outdated.

  This guide provides a step by step tutorial, the codes are taken from [Node.js Express.js
  Demo](https://github.com/RetellAI/retell-backend-node-demo) /
  [Python FastAPI Demo](https://github.com/RetellAI/python-backend-demo).
</Warning>

<Note>Incoming requests by only allowlist these Retell IP addresses: `100.20.5.228`</Note>

### Understanding WebSockets

Unlike the request-response model of HTTPS, WebSockets maintain an open
connection between the client and server. This facilitates two-way message
exchange without needing to reestablish connections, enabling faster data streaming. For more details on
WebSockets, check out
[this blog](https://www.wallarm.com/what/a-simple-explanation-of-what-a-websocket-is) and
[Websocket API Doc](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API).

### Understand Communication Protocol

We have defined [this protocol](/api-references/llm-websocket) that our server
would communicate with your server in. We recommend reading this first before following the guide.

Generally, the protocol requires:

* Your server to send the first message: send empty response to let user speak first.
* We will send live transcripts to your server, and expect responses when we need to.
* You will stream what you want your agent to say to our server, and we will speak it out.

### Step 1: Add a basic websocket endpoint to your server

In this step, you will add a basic websocket endpoint to your express server to
receive message.

If you already have a server up and running, you can add the following code next to your other routes.

<CodeGroup>
  ```javascript Node.js theme={null}
  import { RawData, WebSocket } from "ws";
  import { Request } from "express";

  var express = require('express');
  var app = express();
  var expressWs = require('express-ws')(app);
  const port = 3000

  // Your other API endpoints
  app.get('/', (req, res) => {
    res.send('Hello World!')
  })

  app.ws("/llm-websocket/:call_id",
    async (ws: WebSocket, req: Request) => {
      // callId is a unique identifier of a call, containing all information about it
      const callId = req.params.call_id;

      // You need to send the first message here, but for now let's skip that.

      ws.on("error", (err) => {
        console.error("Error received in LLM websocket client: ", err);
      });
      ws.on("message", async (data: RawData, isBinary: boolean) => {
        // Retell server will send transcript from caller along with other information
        // You will be adding code to process and respond here
        console.log(data);
      });
    },
  );

  app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
  });

  ```

  ```python Python theme={null}
  import json
  import os
  from dotenv import load_dotenv
  from fastapi import FastAPI, Request, WebSocket
  from fastapi.responses import JSONResponse, PlainTextResponse
  from fastapi.websockets import WebSocketState

  app = FastAPI()

  @app.websocket("/llm-websocket/{call_id}")
  async def websocket_handler(websocket: WebSocket, call_id: str):
      await websocket.accept()
      # A unique call id is the identifier of each call
      print(f"Handle llm ws for: {call_id}")

      # You need to send the first message here, but for now let's skip that.

      # listen for new updates
      try:
          while True:
              message = await websocket.receive_text()
              print(message);
      except Exception as e:
          print(f'LLM WebSocket error for {call_id}: {e}')
      finally:
          try:
              await websocket.close()
          except RuntimeError as e:
              print(f"Websocket already closed for {call_id}")
          print(f"Closing llm ws for: {call_id}")

  ```
</CodeGroup>

Using postman, You can send websocket call to your localhost. First click
"Connect", then enter "Hello" in Message tab and click "Send".

<Frame>
  <img />
</Frame>

You should be able to receive the message in your server

<Frame>
  <img />
</Frame>

### Step 2: Create a Dummy Response System

In this step, You will not connect with your LLM yet. Instead, let's just build
a dummy response system who can greet with "How may I help you?", and reply
every users' questions with "I am sorry, can you say that again?".

Don't worry about the dumb agent, we will connect your LLM and make it smart
later.

<CodeGroup>
  ```javascript Node.js theme={null}
  import { WebSocket } from "ws";

  interface Utterance {
    role: "agent" | "user";
    content: string;
  }

  // LLM Websocket Request Object
  export interface RetellRequest {
    response_id?: number;
    transcript: Utterance[];
    interaction_type: "update_only" | "response_required" | "reminder_required";
  }

  // LLM Websocket Response Object
  export interface RetellResponse {
    response_id?: number;
    content: string;
    content_complete: boolean;
    end_call: boolean;
  }

  export class LLMDummyMock {
    constructor() {
    }

    // First sentence requested
    BeginMessage(ws: WebSocket) {
      const res: RetellResponse = {
        response_id: 0,
        content: "How may I help you?",
        content_complete: true,
        end_call: false,
      };
      ws.send(JSON.stringify(res));
    }

    async DraftResponse(request: RetellRequest, ws: WebSocket) {
      if (request.interaction_type === "update_only") {
        // process live transcript update if needed
        return;
      }

      try {
        const res: RetellResponse = {
          response_id: request.response_id,
          content: "I am sorry, can you say that again?",
          content_complete: true,
          end_call: false,
        };
        ws.send(JSON.stringify(res));
      } catch (err) {
        console.error("Error in gpt stream: ", err);
      }
    }
  }
  ```

  ```python Python theme={null}
  import os

  beginSentence = "How may I help you?"

  class LlmDummyMock:
      def __init__(self):
          pass
      
      def draft_begin_message(self):
          return {
              "response_id": 0,
              "content": beginSentence,
              "content_complete": True,
              "end_call": False,
          }

      def draft_response(self, request):      
          yield {
              "response_id": request['response_id'],
              "content": "I am sorry, can you say that again?",
              "content_complete": True,
              "end_call": False,
          }
  ```
</CodeGroup>

Update your websocket endpoint. After receiving "message" event, you will call
`llmClient.DraftResponse()` to get response.

<CodeGroup>
  ```javascript Node.js theme={null}
  // Remember to import the dummy class you wrote

  app.ws("/llm-websocket/:call_id",
    async (ws: WebSocket, req: Request) => {
      const callId = req.params.call_id;
      const llmClient = new LlmDummyMock();

      ws.on("error", (err: Error) => {
        console.error("Error received in LLM websocket client: ", err);
      });

      // Send Begin message
      llmClient.BeginMessage(ws);

      ws.on("message", async (data: RawData, isBinary: boolean) => {
        if (isBinary) {
          console.error("Got binary message instead of text in websocket.");
          ws.close(1002, "Cannot find corresponding Retell LLM.");
        }
        try {
          const request: RetellRequest = JSON.parse(data.toString());
          // LLM will think about a response
          llmClient.DraftResponse(request, ws);
        } catch (err) {
          console.error("Error in parsing LLM websocket message: ", err);
          ws.close(1002, "Cannot parse incoming message.");
        }
      });
    },
  );
  ```

  ```python Python theme={null}
  # remember to import the dummy class you just wrote

  @app.websocket("/llm-websocket/{call_id}")
  async def websocket_handler(websocket: WebSocket, call_id: str):
      await websocket.accept()
      print(f"Handle llm ws for: {call_id}")
      
      llm_client = LlmDummyMock()

      # send first message to signal ready of server
      response_id = 0
      first_event = llm_client.draft_begin_message()
      await websocket.send_text(json.dumps(first_event))

      async def stream_response(request):
          nonlocal response_id
          for event in llm_client.draft_response(request):
              await websocket.send_text(json.dumps(event))
              if request['response_id'] < response_id:
                  return # new response needed, abandon this one
      try:
          while True:
              message = await websocket.receive_text()
              request = json.loads(message)
              # print out transcript
              os.system('cls' if os.name == 'nt' else 'clear')
              print(json.dumps(request, indent=4))
              
              if 'response_id' not in request:
                  continue # no response needed, process live transcript update if needed
              response_id = request['response_id']
              asyncio.create_task(stream_response(request))
      except WebSocketDisconnect:
          print(f"LLM WebSocket disconnected for {call_id}")
      except Exception as e:
          print(f'LLM WebSocket error for {call_id}: {e}')
      finally:
          print(f"LLM WebSocket connection closed for {call_id}")
  ```
</CodeGroup>

### Step 3: Test your basic agent on Dashboard

At this point, you are ready to make your basic agent speak in the dashboard.

1. If you deploy your server, you can get a url using your domain:
   `wss://your_domain_name/llm-websocket/`

2. If you want to test your code locally, you can use
   [ngrok](https://ngrok.com/) to generate a production url forwarding requests
   to your local endpoints. You can watch this
   [video](https://youtu.be/Tz969io9cPc?si=Qod-lRgUhILG-4_K\&t=344) to learn how
   to do that. After getting your ngrok url, you will have a url
   `wss://xxxxx.ngrok-free.app/llm-websocket/`

Add either the ngrok url or your production url into the dashboard

<Frame>
  <img />
</Frame>

**Click "Make a web call" and you should be able to hear the agent talking. It
will greet with "How may I help you?", and reply every users' questions with "I
am sorry, can you say that again?".**

Congrats! You just connect your websocket to our server. Let's connect to your
LLM to make the agent smarter.

<Tip>
  If you still cannot hear the agent talking, check out our [troubleshooting
  guide](/integrate-llm/troubleshooting)
</Tip>


# Troubleshooting Guide
Source: https://docs.retellai.com/integrate-llm/troubleshooting



## Problem: Cannot Hear Audio After Entering Your Websocket URL

If you've entered your websocket URL into the dashboard and cannot hear audio, here are a few troubleshooting steps you can try.

<Frame>
  <img />
</Frame>

### Step 1: Test Connection with Postman

First, attempt to connect to your websocket URL endpoint using Postman. This step helps verify if the websocket connection is successfully established.

* **How to Test:**

  1. Open Postman and select the option to create a new WebSocket request.
  2. Enter your WebSocket URL and click on "Connect".
  3. Once connected, navigate to the "Message" tab, enter "Hello", and click "Send".

  You should receive the message back in your server indicating a successful connection.

<Frame>
  <img />
</Frame>

### Step 2: Verify Endpoint Protocol

It's important to ensure that your URL protocol matches the type of connection.

* **HTTPS Endpoints:** Use `wss://` prefix for secure WebSocket connections.
* **HTTP Endpoints:** Use `ws://` prefix for standard WebSocket connections.

### Step 3: Check for Trailing Slash

Some server setups might not allow a trailing slash in the URL. Make sure to check your URL format carefully.

* **Correct Format:** `https://example.com/websocket`
* **Incorrect Format (sometimes):** `https://example.com/websocket/`

By following these steps, you should be able to diagnose and potentially fix the issue preventing audio from playing through your WebSocket URL. If problems persist, consider consulting your server or network administrator for further assistance.

### Step 4: Check for Retell Server Response

* Add logging in your [websocket code](https://github.com/RetellAI/retell-backend-node-demo/blob/ab3b5e1857d2866effece0927ad55f4be1500b55/src/server.ts#L79) to see if the websocket is connected

* Add logging in your [websocket message code](https://github.com/RetellAI/retell-backend-node-demo/blob/ab3b5e1857d2866effece0927ad55f4be1500b55/src/server.ts#L92) to check if you receive the message from Retell server

## Problem: If my call always disconnects automatically after a couple seconds

* Add loggin in your backend to check if you send "end\_call=true" at any point.
* Check if you server setup support WebSocket. For example, Vercel edge functions and serverless functions
  cannot act as a websocket server.

## Problem: If my call always disconnects automatically after 5min / 10min

Check the server vendor you have, and see if you are getting automatically timed out for it.

For example, Replit non reserved instance would timeout at 5min.


# HubSpot Integration
Source: https://docs.retellai.com/integrations/hubspot

Set up and use the Retell AI application in HubSpot to automate outbound phone calls using voice agents

This guide provides instructions for setting up and using the **Retell AI** application within **HubSpot** to automate outbound phone calls using voice agents.

<Card title="Install Retell AI for HubSpot" icon="download" href="https://app.hubspot.com/marketplace/46771873/listing/retell-ai">
  Click here to open the Retell AI integration in HubSpot Marketplace.
</Card>

## Overview

The Retell AI application enables the **Make a Phone Call** action in HubSpot workflows. This action creates an outbound call using your AI agents and pauses the workflow until the call is finished.

Once a call is completed, HubSpot is automatically updated with:

* **Activity Timeline**: Post-call analysis and call summary
* **Call Log**: Recording and detailed call transcript
* **Company Record**: Call logs also appear on the associated company timeline

## Installing the Application

<Steps>
  <Step title="Initiate installation">
    Click **Connect app** when prompted during installation.

    <Frame>
      <img alt="HubSpot app installation prompt" />
    </Frame>
  </Step>

  <Step title="Complete external integration form">
    You will be redirected to an external integration form.

    <Frame>
      <img alt="External integration form" />
    </Frame>
  </Step>

  <Step title="Sign up for Retell AI">
    Sign up on the Retell AI website to access your dashboard if you don't already have an account.
  </Step>

  <Step title="Get your API key">
    Navigate to **Settings → API Keys** in the Retell AI Dashboard.

    Copy the **Secret Key (Webhook)** and paste it into the **Retell API Key** field on the installation form.

    <Frame>
      <img alt="Retell AI API Keys settings" />
    </Frame>
  </Step>

  <Step title="Configure webhook URL">
    Copy the **Webhook URL** provided in the form and paste it into the Webhooks section of your Retell Dashboard (**Settings → Webhooks**).

    <Frame>
      <img alt="Retell AI Webhooks settings" />
    </Frame>
  </Step>

  <Step title="Save and return to HubSpot">
    Click **Save** to submit the form, then close the page and return to HubSpot.
  </Step>
</Steps>

## Using the Application

HubSpot workflows allow you to automatically trigger outbound calls based on various events. Common use cases include:

* **New lead qualification**: Call leads immediately after they submit a form to qualify interest
* **New contact created**: Reach out to new contacts added to your CRM
* **Deal stage changes**: Follow up when a deal moves to a specific stage
* **Re-engagement**: Call contacts who haven't been active for a set period
* **Appointment reminders**: Confirm upcoming meetings or demos
* **Post-purchase follow-up**: Check in with customers after a purchase

<Note>
  You must have a Retell AI account and an agent with a connected phone number.
</Note>

### Step 1: Creating the HubSpot Workflow

<Steps>
  <Step title="Create a new workflow">
    Navigate to **Automation → Workflows** in HubSpot.

    Create a new workflow and choose your trigger based on your use case:

    * **Form submission**: Trigger when a lead fills out a specific form
    * **Record created**: Trigger when a new contact is added to your CRM
    * **Property value change**: Trigger when a deal stage or lead status changes
    * **Date-based**: Trigger based on a specific date property (e.g., appointment date)

    For this example, set the trigger to **Data Values → Record Created**.

    <Frame>
      <img alt="Create workflow with Record Created trigger" />
    </Frame>
  </Step>

  <Step title="Add phone number condition">
    Add a condition for **Phone number is known**. This ensures the workflow only triggers for contacts with valid phone numbers, preventing failed call attempts.

    You can also add additional conditions to further qualify which contacts receive calls:

    * **Lead status**: Only call contacts with a specific lead status
    * **Lifecycle stage**: Target contacts at a particular stage (e.g., "Lead" or "Marketing Qualified Lead")
    * **Contact owner**: Route calls based on the assigned sales rep
    * **Custom properties**: Filter based on your business-specific criteria

    <Frame>
      <img alt="Add phone number condition" />
    </Frame>

    The final trigger should look like the following:

    <Frame>
      <img alt="Phone number condition configuration" />
    </Frame>
  </Step>

  <Step title="Add Retell AI action">
    Click the **(+)** button to add an action. Select **Retell AI → Make a Phone Call** under "Integrated apps".

    <Frame>
      <img alt="Add Retell AI Make a Phone Call action" />
    </Frame>
  </Step>

  <Step title="Configure the call form">
    Configure the call form with the following settings:

    * **From**: Select the Retell AI agent/phone number
    * **To**: Select the contact's phone number token
    * **Dynamic Variables** (Optional): Pass data like the contact's name using JSON format. Ensure all values are surrounded by quotes.

    <Frame>
      <img alt="Call form configuration" />
    </Frame>

    <br />

    <Frame>
      <img alt="From field selection" />
    </Frame>

    <br />

    <Frame>
      <img alt="To field selection" />
    </Frame>

    <br />

    <Frame>
      <img alt="Dynamic variables configuration" />
    </Frame>

    Click **Save**.
  </Step>

  <Step title="Add subsequent actions based on call outcome">
    After the call completes, you can branch your workflow based on the call outcome to automate follow-up actions.

    Use the **Call Success** output from the Retell AI action to create branches:

    **If call was successful:**

    * Send a follow-up email with next steps
    * Create a task for the sales rep to review the call
    * Update the contact's lifecycle stage
    * Add the contact to a nurture sequence

    **If call was unsuccessful** (no answer, voicemail, etc.):

    * Schedule a retry call for a later time
    * Send an SMS or email as an alternative touchpoint
    * Add to a "needs follow-up" list

    <Frame>
      <img alt="Branching workflow based on call outcome" />
    </Frame>

    <Tip>
      You can also use other call outputs like **User Sentiment** or **Call Outcome** to create more granular branching logic.
    </Tip>
  </Step>

  <Step title="Publish the workflow">
    Review and click **Review and publish** to activate.
  </Step>
</Steps>

### Step 2: Viewing Call Results in HubSpot

After a contact is enrolled in the workflow and the call completes, you can view the results directly in HubSpot.

<Steps>
  <Step title="Open the contact record">
    Navigate to **CRM → Contacts** and open the contact that was enrolled in the workflow.

    <Tip>
      You can also find recently called contacts by filtering the contact list by the workflow enrollment date or checking the workflow history.
    </Tip>

    <Frame>
      <img alt="Activity tab with filters" />
    </Frame>
  </Step>

  <Step title="View call analysis">
    Check the contact's **Activity** tab to view the **Call Analysis**.

    <Note>
      Ensure your activity filters include "Retell AI" as shown below:
    </Note>

    <Frame>
      <img alt="Activity filters including Retell AI" />
    </Frame>

    Each call displays two types of analysis data:

    **Default Call Results** — Automatically generated for every call:

    * Summary
    * Duration
    * Voicemail detection
    * User Sentiment
    * Call Outcome

    **Custom Analysis** — Additional insights you configure in Retell AI using [Post-Call Analysis](/features/post-call-analysis-overview):

    * Lead qualification status
    * Custom scoring metrics
    * Business-specific data extraction
    * Any other fields you define

    <Frame>
      <img alt="Call Analysis in Activity tab" />
    </Frame>
  </Step>

  <Step title="View call log and recording">
    Check the **Calls** tab to view the full **Call Log** and recording.

    <Frame>
      <img alt="Call Log with recording" />
    </Frame>
  </Step>
</Steps>

## Uninstalling the Application

<Steps>
  <Step title="Navigate to Connected Apps">
    Go to **Connected Apps** and select **Retell AI**.
  </Step>

  <Step title="Access General Settings">
    Navigate to the **General Settings** tab.

    <Frame>
      <img alt="Retell AI General Settings tab" />
    </Frame>
  </Step>

  <Step title="Uninstall the application">
    Click **Uninstall**.

    <Frame>
      <img alt="Uninstall Retell AI application" />
    </Frame>

    <Warning>
      Your data will be deleted from Retell AI records and the app will be removed from HubSpot.
    </Warning>
  </Step>
</Steps>


# Audio Basics
Source: https://docs.retellai.com/knowledge/audio-basics



### How is Audio Represented Digitally

Sound waves are captured by a microphone, which converts the acoustic energy
into electrical analog signals. The analog signals are then fed into an ADC
(Analog-to-Digital Conversion). Here, two critical processes occur - sampling
and quantization.

<Card title="Sampling">
  <Steps>
    <Step title="Definition">
      Sampling is the process of measuring the amplitude of an analog signal at
      regular intervals. These intervals are determined by the sample rate,
      expressed in Hertz (Hz). For example, a sample rate of 44.1 kHz means the
      signal is sampled 44,100 times per second.
    </Step>

    <Step title="Purpose">
      By sampling the audio signal, we create a series of discrete data points
      that approximate the continuous analog waveform.
    </Step>

    <Step title="Implication">
      The Nyquist Theorem states that the sample rate must be at least twice the
      highest frequency component in the audio signal to accurately reconstruct
      the original signal. For example, human hearing typically ranges up to 20
      kHz, hence the standard CD sample rate of 44.1 kHz.
    </Step>
  </Steps>
</Card>

<Card title="Quantization">
  <Steps>
    <Step title="Definition">
      Quantization is the process of converting each sampled amplitude value
      into a digital value. This involves assigning a specific numerical value
      (quantization level) to each sample, based on its amplitude.
    </Step>

    <Step title="Purpose">
      The range of possible amplitude values is divided into discrete steps.
      Each step is assigned a digital value. The bit depth determines the number
      of possible quantization levels. For instance, a 16-bit system can
      represent 65,536 (2^16) different levels.
    </Step>

    <Step title="Implication">
      Quantization introduces a small amount of error, known as quantization
      noise, because the process involves rounding the true amplitude value to
      the nearest quantization level. Higher bit depths can reduce this error,
      leading to higher fidelity audio.
    </Step>
  </Steps>
</Card>

### Terminology

<Tab title="Sample Rate">
  The sample rate is the number of samples of audio carried per second. It's
  measured in Hertz (Hz).
</Tab>

<Tab title="Channel Count">
  This refers to the number of separate audio channels (e.g., mono, stereo,
  surround sound) in the recording. <br />
  Mono means single channel. All audio is combined into one channel.
</Tab>

<Tab title="Bit Depth">
  Bit depth refers to the number of bits used to represent each audio sample.
</Tab>

### Audio Encoding

Audio encoding refers to the process of converting audio data into a format that
can be easily stored, transmitted, and decoded by audio playback devices. This
process often involves compression to reduce file size while trying to maintain
the quality of the original audio. There are several popular audio encoding
formats, each with its own specific use cases and characteristics.

Here're some examples:

<Tabs>
  <Tab title="PCM">
    * `Description`: PCM (Pulse Code Modulation) is the most straightforward form of digital audio
      encoding. It represents the amplitude of the audio signal at uniformly spaced
      intervals.

    * `Usage`: It's the standard form of digital audio in computers, CDs, digital
      telephony, and other digital audio applications.
  </Tab>

  <Tab title="MP3">
    * `Description`: MP3 (MPEG Audio Layer III) is a lossy compression format that significantly reduces
      file size by removing audio data considered less important to human hearing.

    * `Usage`: It was widely used for music distribution and playback due to its
      ability to reduce file size while maintaining a decent level of audio quality.
  </Tab>

  <Tab title="AAC">
    * `Description`: AAC (Advanced Audio Coding) is a more advanced form of lossy compression than MP3,
      offering better audio quality at similar bitrates.

    * `Usage`: It’s commonly used in online streaming services, Apple's iTunes, and
      YouTube.
  </Tab>

  <Tab title="Opus">
    * `Description`: Opus is a versatile, open standard audio codec. It provides
      low latency and high-quality audio.

    * `Usage`: It’s widely used for real-time applications like video conferencing,
      VoIP, and streaming.
  </Tab>

  <Tab title="μ-law">
    * `Description`: μ-law (mu-law or ulaw) encoding is a non-linear audio encoding technique used
      in telephony. It compresses dynamic range, emphasizing quieter sounds for
      improved clarity.

    * `Usage`: Predominantly used in North American and Japanese telephone systems,
      it's integral to the G.711 telephony standard, enhancing voice transmission
      quality.
  </Tab>
</Tabs>

Note that audio encoding is not the same as audio format. An audio format refers
to the entire structure of the audio file, which includes the encoding, but also
encompasses other elements like metadata, file headers, and containers. For
example, a WAV file typically uses PCM encoding, and has its own header that
specifies audio sample rate, number of samples, etc.

### PCM Audio Representation

When audio is played, it is typically decoded into PCM (Pulse Code Modulation).
This process is true for most digital audio systems, regardless of the original
audio format or encoding method.

There are generally two types of PCM audio representation:

* `Float 32 Array`: It uses a 32-bit floating-point format to represent each
  sample. When capturing mic stream and setting up playback in web environment,
  PCM will be represented in this format.
* `Unsigned 8 Array`: It uses an array of 8-bit unsigned integers (aka bytes),
  and each sample can be multiple bytes. For example, for a mono PCM audio with
  bit depth of 16 bit, each sample will be two bytes. This is a lower-level
  representation and is often used in programming for audio processing.

Here's the code snippet to convert between these two format:

```javascript theme={null}
export function convertUnsigned8ToFloat32(array: Uint8Array): Float32Array {
  const targetArray = new Float32Array(array.byteLength / 2);

  // A DataView is used to read our 16-bit little-endian samples
  // out of the Uint8Array buffer
  const sourceDataView = new DataView(array.buffer);

  // Loop through, get values, and divide by 32,768
  for (let i = 0; i < targetArray.length; i++) {
    targetArray[i] = sourceDataView.getInt16(i * 2, true) / Math.pow(2, 16 - 1);
  }
  return targetArray;
}

export function convertFloat32ToUnsigned8(array: Float32Array): Uint8Array {
  const buffer = new ArrayBuffer(array.length * 2);
  const view = new DataView(buffer);

  for (let i = 0; i < array.length; i++) {
    const value = array[i] * 32768;
    view.setInt16(i * 2, value, true); // true for little-endian
  }

  return new Uint8Array(buffer);
}
```

### Audio Spec Retell AI Use

* `Phone Calls`: Different telephony providers have different audio codecs.
  Our telephony integrations handle that for you internally, and you don't need to worry about
  encoding and decoding.
* `Web Calls`: The [frontend web JS SDK](https://www.npmjs.com/package/retell-client-js-sdk)
  abstracts away audio complexity for you. The user audio
  is captured in PCM format and sent to the backend for processing.


# Debug call transfer failure
Source: https://docs.retellai.com/reliability/call-performance



When experiencing call transfer issues, follow these troubleshooting steps to identify and resolve common problems.

## Agent-Specific Troubleshooting

### For Single/Multi-Prompt Agents

If call transfer is not triggered in your single or multi-prompt agent:

<Steps>
  <Step title="Verify transfer_call function implementation">
    1. Check your agent configuration
    2. Confirm that you've added the transfer\_call function to your agent's function list
    3. Visit [Function Calling Guide](build/single-multi-prompt/function-calling) for more details on implementing the function
  </Step>

  <Step title="Review transfer conditions">
    1. Update your agent's prompt to clearly define transfer conditions
    2. Ensure the transfer\_call function description is specific and unambiguous
    3. Test with sample scenarios to validate transfer triggers
  </Step>
</Steps>

For more detailed guidance on specific features, visit [Call Transfer Setup](../build/single-multi-prompt/transfer-call).

### For Conversation Flow Agents

If call transfer is not triggered in your conversation flow agent:

<Steps>
  <Step title="Check transfer node configuration">
    1. Verify you have a transfer node in your conversation flow
    2. Ensure the transfer node is properly connected to other nodes
    3. Check that transition conditions are correctly set up
  </Step>

  <Step title="Review transfer node settings">
    1. Confirm the transfer destination is correctly configured
    2. Verify the transfer conditions in the node are clear and specific
    3. Test the flow to ensure the transfer node is reachable
  </Step>
</Steps>

For more detailed guidance, visit [Conversation Flow Transfer Setup](../build/conversation-flow/transfer-node).

## General Troubleshooting

### Call Type Verification

<Note>Call transfer is only supported for phone calls, **not web calls**</Note>

### If Call Transfer is Triggered but Failed

* **Telephony issues**: Call transfer is similar to placing an outbound call, and failures occur for similar reasons as outbound call failures. The SIP connection log is available in the call logs and is useful for diagnosing the failure reason.
  Please refer to [Understand Reasons for Outbound Call Failure](/reliability/debug-outbound-call) for more details.
* **Could not detect human**: If human detection is enabled, the call may fail if a human is not successfully detected. Possible reasons include:
  * No human was actually present (e.g. it was an IVR or voicemail).
  * The other party spoke, but only after the detection timeout expired.
  * The speech was too similar to an IVR or voicemail and was not recognized as human.


# Check actual latency
Source: https://docs.retellai.com/reliability/check-actual-latency

Monitor per-call latency through the dashboard or the Get Call API

You can monitor the latency of individual calls in the "Call History" section.

<Frame>
  <img alt="Call history page showing per-call latency metrics" />
</Frame>

### Understanding latency metrics

End-to-end latency measures the total time from when the user stops speaking until the AI agent begins responding. This includes processing time, network delays, and model inference time.

### Key metrics explained

* **P90 (90th Percentile)**: 90% of calls have latency below this value.
* **Median (50th Percentile)**: Half of the calls have latency less than this value.
* **Min**: The fastest response time achieved in any call.

## Retrieve latency via the API

You can also retrieve detailed latency breakdowns programmatically using the [Get Call API](/api-references/get-call). After a call ends, the response includes a `latency` object with per-component metrics.

<CodeGroup>
  ```bash cURL theme={null}
  curl -X GET "https://api.retellai.com/v2/get-call/CALL_ID" \
    -H "Authorization: Bearer YOUR_API_KEY"
  ```

  ```python Python theme={null}
  from retell import Retell

  client = Retell(api_key="YOUR_API_KEY")
  call = client.call.retrieve("CALL_ID")
  print(call.latency)
  ```

  ```javascript Node.js theme={null}
  import Retell from "retell-ai";

  const client = new Retell({ apiKey: "YOUR_API_KEY" });
  const call = await client.call.retrieve("CALL_ID");
  console.log(call.latency);
  ```
</CodeGroup>

### Latency breakdown fields

The `latency` object contains the following components. Not all fields are present on every call — availability depends on the call type and features used.

| Field                       | Description                                                                                                                                                                 |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `e2e`                       | End-to-end latency from when the user stops talking to when the agent starts talking. Does not account for network trip time from the Retell server to the user's frontend. |
| `asr`                       | Transcription latency — the difference between the duration of audio chunks streamed and the duration of the transcribed portion.                                           |
| `llm`                       | LLM latency from the start of the LLM call to the first speakable chunk received. When using a custom LLM, this includes the websocket roundtrip time.                      |
| `llm_websocket_network_rtt` | Websocket roundtrip latency between your server and the Retell server. Only populated for calls using a custom LLM.                                                         |
| `tts`                       | Text-to-speech latency from triggering TTS to the first audio byte received.                                                                                                |
| `knowledge_base`            | Knowledge base retrieval latency from triggering retrieval to receiving all relevant context. Only populated when the agent uses the knowledge base feature.                |
| `s2s`                       | Speech-to-speech latency from requesting a response to the first byte received. Only populated for calls using a speech-to-speech model (e.g., Realtime API).               |

Each component is an object with these statistical fields:

| Field    | Type      | Description                                        |
| -------- | --------- | -------------------------------------------------- |
| `p50`    | number    | 50th percentile (median) latency in milliseconds   |
| `p90`    | number    | 90th percentile latency in milliseconds            |
| `p95`    | number    | 95th percentile latency in milliseconds            |
| `p99`    | number    | 99th percentile latency in milliseconds            |
| `min`    | number    | Minimum latency in milliseconds                    |
| `max`    | number    | Maximum latency in milliseconds                    |
| `num`    | number    | Number of data points tracked                      |
| `values` | number\[] | All individual latency data points in milliseconds |

### Example response

Here is an example of the `latency` portion of a Get Call response:

```json theme={null}
{
  "latency": {
    "e2e": {
      "p50": 800,
      "p90": 1200,
      "p95": 1500,
      "p99": 2500,
      "min": 500,
      "max": 2700,
      "num": 10,
      "values": [500, 620, 780, 800, 850, 900, 1100, 1200, 1500, 2700]
    },
    "llm": {
      "p50": 400,
      "p90": 650,
      "p95": 800,
      "p99": 1200,
      "min": 250,
      "max": 1300,
      "num": 10,
      "values": [250, 310, 380, 400, 420, 500, 600, 650, 800, 1300]
    },
    "tts": {
      "p50": 150,
      "p90": 250,
      "p95": 300,
      "p99": 400,
      "min": 80,
      "max": 420,
      "num": 10,
      "values": [80, 100, 130, 150, 160, 200, 230, 250, 300, 420]
    }
  }
}
```


# Check estimated latency
Source: https://docs.retellai.com/reliability/check-estimated-latency



Retell platform achieves latency as low as 600ms, measured from when the user stops speaking to when the AI agent begins responding.

In the agent detail page, under the "Estimated Latency" section, you can view the average latency for the agent.

<Frame>
  <img alt="Estimated Latency" />
</Frame>

Please note that certain settings will increase latency. These settings are marked with a turtle icon.

<Frame>
  <img alt="Increase Latency" />
</Frame>


# Debug call disconnection
Source: https://docs.retellai.com/reliability/debug-call-disconnect

Diagnose call disconnection reasons.

You can check the reason why a call is disconnected through the Retell Dashboard or by using the [get-call](/api-references/get-call) API endpoint.

<Frame>
  <img />
</Frame>

## Diagnosing Disconnection Reasons

<Note>Please note that when phone numbers engage in a lot of short calls in a short period, they might be marked as spam at
carrier level, which in turn leads to the number being blocked and showing up as `dial_failed`.</Note>

| Disconnection Reason                   | Call Status    | Description                                                                                                                                                                                              |
| -------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_hangup`                          | ended          | Expected behavior, user hung up the call.                                                                                                                                                                |
| `agent_hangup`                         | ended          | Expected behavior, AI agent hung up the call.                                                                                                                                                            |
| `call_transfer`                        | ended          | Expected behavior, AI agent transferred the call.                                                                                                                                                        |
| `voicemail_reached`                    | ended          | Expected behavior, if AI agent is configured with voicemail settings, and voicemail is reached.                                                                                                          |
| `ivr_reached`                          | ended          | Expected behavior, if AI agent is configured to hang up when encountering an IVR system, and IVR is reached.                                                                                             |
| `inactivity`                           | ended          | Expected behavior, call was terminated due to the "end\_call\_after\_silence\_ms" setting reached after long inactivity.                                                                                 |
| `max_duration_reached`                 | ended          | Expected behavior, call was terminated due to maximum duration reached.                                                                                                                                  |
| `dial_busy`                            | not\_connected | Outbound call not connected, the number dialed is busy.                                                                                                                                                  |
| `dial_failed`                          | not\_connected | Outbound call not connected, dialing failed with no or unknown sip error code.                                                                                                                           |
| `dial_no_answer`                       | not\_connected | Outbound call not connected, the number dialed did not answer.                                                                                                                                           |
| `invalid_destination`                  | not\_connected | Outbound call not connected, the number dialed is invalid. Can be due to spaces or invalid characters in the number. Or it can be your telephony provider requiring specific format (like e.164 format). |
| `telephony_provider_permission_denied` | not\_connected | Outbound call not connected, the sip trunk credentials are not authenticated.                                                                                                                            |
| `telephony_provider_unavailable`       | not\_connected | Outbound call not connected, the telephony provider is unavailable.                                                                                                                                      |
| `sip_routing_error`                    | not\_connected | Outbound call not connected, the sip routing is going over too many hops or is in a loop.                                                                                                                |
| `marked_as_spam`                       | not\_connected | Outbound call not connected, the number dialed is marked as spam. See [Spam Likely Overview](/build/telephony/call_efficiency_overview).                                                                 |
| `user_declined`                        | not\_connected | Outbound call not connected, user declined the call.                                                                                                                                                     |
| `concurrency_limit_reached`            | error          | Error, concurrency limit reached, add a retry with exponential backoff. Or consider enterprise plan.                                                                                                     |
| `no_concurrency_fallback`              | ended          | Inbound call could not get a concurrency slot and was transferred to the configured fallback number.                                                                                                     |
| `no_valid_payment`                     | error          | Error, no valid payment registered on file, or service shut down due to bill overdue.                                                                                                                    |
| `scam_detected`                        | error          | Error, scam detected for that particular agent.                                                                                                                                                          |
| `error_llm_websocket_open`             | error          | Error, LLM websocket did not open between Retell server and your backend. Likely because the Custom LLM URL is incorrect or your LLM server is unreachable.                                              |
| `error_llm_websocket_lost_connection`  | error          | Error, LLM websocket connection broke during the call.                                                                                                                                                   |
| `error_llm_websocket_runtime`          | error          | Error, LLM websocket received a closing signal other than `1000` from your server.                                                                                                                       |
| `error_llm_websocket_corrupt_payload`  | error          | Error, LLM websocket received unspecified payload.                                                                                                                                                       |
| `error_no_audio_received`              | error          | Error, has not received audio from Twilio or web frontend for a while after connection has established.                                                                                                  |
| `error_asr`                            | error          | Error, Retell's ASR encountered a problem.                                                                                                                                                               |
| `error_retell`                         | error          | Error, unspecified Retell side problem.                                                                                                                                                                  |
| `error_unknown`                        | error          | Error, unknown error.                                                                                                                                                                                    |
| `error_user_not_joined`                | error          | Error, user did not join web call within 30s after calling startWebCall.                                                                                                                                 |
| `registered_call_timeout`              | error          | Error, phone call is 5 minutes or more apart from registration.                                                                                                                                          |


# Debug SIP calls using PCAP file
Source: https://docs.retellai.com/reliability/debug-calls-pcap

Step-by-step guide to analyze SIP, RTP, and DTMF traffic using Wireshark and tshark.

PCAP (Packet Capture) files record raw network traffic and are invaluable for diagnosing SIP call issues — including codec negotiation failures, audio quality problems, one-way audio, and missed DTMF tones. This guide walks through capturing and analyzing these files.

## Prerequisites

Install the tools you need:

* **[Wireshark](https://www.wireshark.org/download.html)** — GUI packet analyzer (includes `tshark` CLI)

Verify installation:

```bash theme={null}
wireshark --version
tshark --version
```

***

## Step 1: Open and filter the PCAP in Wireshark

Open the file in Wireshark:
Once Wireshark is installed you can double click on the PCAP file and your system should open it automatically using Wireshak application. Alternatively, you can open it by using the following command:

```bash theme={null}
wireshark call_capture.pcap
```

### Filter for SIP traffic only

In the **Display Filter** bar, enter:

```
sip
```

<Frame>
  <img alt="Wireshark displaying SIP traffic after applying the sip display filter" />
</Frame>

This shows all SIP messages: `INVITE`, `100 Trying`, `180 Ringing`, `200 OK`, `ACK`, `BYE`, `CANCEL`, etc.

### Filter for a specific call (optional)

If you need to isolate a single call, find the `Call-ID` value in any SIP packet, then filter on it:

```
sip.Call-ID == "abc123@192.168.1.1"
```

### Filter for RTP media streams

```
rtp
```

Or combine SIP and RTP:

```
sip or rtp
```

***

## Step 2: Reconstruct the SIP call flow

After filtering SIP call(s), you can view the sequence (ladder) diagram by selecting **Telephony → VoIP Calls**:

<Frame>
  <img alt="Wireshark Telephony menu with VoIP Calls option selected" />
</Frame>

Select the call(s) from the popup window and click **Flow Sequence**:

<Frame>
  <img alt="VoIP Calls popup with Flow Sequence button" />
</Frame>

After clicking **Flow Sequence**, a new window opens with the ladder diagram showing the complete message exchange between endpoints:

<Frame>
  <img alt="SIP flow sequence ladder diagram with INVITE, 100 Trying, 180 Ringing, 200 OK, ACK, and BYE messages" />
</Frame>

The diagram shows the full call flow — `INVITE` → `100 Trying` → `180 Ringing` → `200 OK` → `ACK` → `BYE`.

### Read a SIP INVITE manually

Click the `INVITE` packet and expand **Session Initiation Protocol** in the packet detail pane. Key fields to inspect:

<Frame>
  <img alt="Wireshark packet detail view of a SIP INVITE showing Request-URI, SIP headers, and SDP parameters including codecs and DTMF negotiation" />
</Frame>

| Field            | What to look for                                            |
| ---------------- | ----------------------------------------------------------- |
| `Request-URI`    | Destination SIP address                                     |
| `From` / `To`    | Caller and callee                                           |
| `Call-ID`        | Unique call identifier                                      |
| `SDP → m=audio`  | Negotiated RTP port and codec list                          |
| `SDP → a=rtpmap` | Codec payload type mappings (e.g., PCMU=0, PCMA=8, G.722=9) |
| `SDP → a=fmtp`   | Codec parameters                                            |

***

## Step 3: Common issues and what to look for

| Symptom                          | What to check in PCAP                                                                                                                                                                                                          |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| One-way audio                    | RTP flowing only in one direction; check both streams i.e check RTP packets for both directions                                                                                                                                |
| No audio at all                  | `m=audio` port in SDP is `0` (call on hold), or RTP packets absent(where RTP is supposed to be captured)                                                                                                                       |
| DTMF not recognized              | Payload type mismatch between INVITE SDP and actual RTP packets                                                                                                                                                                |
| Audio choppy or robotic          | High jitter or packet loss in **RTP Streams**                                                                                                                                                                                  |
| Call drops unexpectedly          | Look for `BYE` or `CANCEL`; check SIP response codes (4xx, 5xx)                                                                                                                                                                |
| Call hung up mid-conversation    | Could be Media Timeout or Callee simply hungup. Look for the party that initiated the `BYE`                                                                                                                                    |
| Codec mismatch                   | SDP `200 OK` `a=rtpmap` differs from INVITE; or RTP payload type not in SDP                                                                                                                                                    |
| SIP auth failure                 | `401/407 Proxy Authentication Required` or `403 Forbidden` in SIP flow                                                                                                                                                         |
| `408/477` response to INVITE     | Remote SIP infrastructure may be unreachable — verify reachability, firewall settings, port (typically 5060 or 5061 for TLS), and SIP URI                                                                                      |
| `486` response to INVITE         | Callee rejected the call. Call maybe retried later                                                                                                                                                                             |
| `500/503/603` response to INVITE | Check remote SIP infrastructure and downstream call routing status such as when call is routed to a downstream carrier for delivery; if you purchased phone numbers through Retell, contact [Retell support](/general/support) |

### Common SIP response code reference

| Code          | Meaning                                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------------------- |
| `100`         | Trying                                                                                                   |
| `180`         | Ringing                                                                                                  |
| `200`         | OK                                                                                                       |
| `401` / `407` | Authentication required                                                                                  |
| `403`         | Forbidden (Auth failure. Caller does not have permission to dial or transfer to the number/endpoint)     |
| `404`         | Not found (wrong number or SIP URI)                                                                      |
| `408`         | Request timeout (Sip message over UDP could not be delivered or the corresponding Sip Response was lost) |
| `477`         | Send failed (Sip TCP or TLS transport error)                                                             |
| `486`         | Busy here (Callee rejected the call)                                                                     |
| `487`         | Request terminated (caller did not pick up)                                                              |
| `500`         | Server internal error                                                                                    |
| `503`         | Service unavailable                                                                                      |
| `603`         | Decline                                                                                                  |

***

## Quick reference: filter cheatsheet

| Goal                 | Wireshark filter                          |
| -------------------- | ----------------------------------------- |
| All SIP              | `sip`                                     |
| Specific Call-ID     | `sip.Call-ID == "id@host"`                |
| SIP INVITE only      | `sip.Method == "INVITE"`                  |
| SIP errors (4xx/5xx) | `sip.Status-Code >= 400`                  |
| All RTP              | `rtp`                                     |
| RFC 2833 DTMF        | `rtp.p_type == 101`                       |
| SIP + RTP combined   | `sip or rtp`                              |
| From specific IP     | `ip.src == 192.168.1.10 and (sip or rtp)` |

***

## Advanced Debugging

The sections below use additional tools:

* **`tcpdump`** — command-line capture (pre-installed on Linux/macOS; see [tcpdump.org](https://www.tcpdump.org/) for other platforms)
* **`sngrep`** — SIP-specific terminal UI (install instructions in the sngrep section below)

### Analyze RTP streams

This applies only when your PCAP file contains RTP media packets. Some captures include SIP signaling only — for example, the PCAP files available on the [Retell call details dashboard](/features/session-history) — in which case RTP and DTMF analysis are not available.

#### View all RTP streams

Go to **Telephony → RTP → RTP Streams**.

Wireshark lists each detected stream with:

| Column               | Description                                     |
| -------------------- | ----------------------------------------------- |
| Source / Destination | IP:port pairs                                   |
| SSRC                 | Synchronization source ID                       |
| Payload type         | Codec ID (e.g., 0 = PCMU, 8 = PCMA, 111 = Opus) |
| Packets              | Total packets in stream                         |
| Lost                 | Packet loss count and percentage                |
| Max jitter           | Maximum inter-packet jitter in ms               |

<Warning>
  High packet loss (>3%) or jitter (>30ms) typically causes degraded audio quality or choppy speech on Retell calls. See [Call Performance](/reliability/call-performance) for remediation steps.
</Warning>

#### Play back RTP audio

1. Select a stream in **RTP Streams**.
2. Click **Analyze → Play Streams**.
3. Wireshark decodes and plays back the audio. This lets you hear exactly what was sent or received.

#### Save RTP audio to a file

In the RTP player, click **Save payload** to export raw audio. You can then open it in [Audacity](https://www.audacityteam.org/) or convert it with [ffmpeg](https://ffmpeg.org/download.html). Install ffmpeg if needed: `brew install ffmpeg` (macOS) or `sudo apt install ffmpeg` (Debian/Ubuntu).

```bash theme={null}
# Convert raw PCMU (G.711 ulaw, 8kHz, mono) to WAV
ffmpeg -f mulaw -ar 8000 -ac 1 -i rtp_payload.raw output.wav
```

***

### Extract and inspect DTMF events

#### Check for DTMF negotiation in SDP

In the `INVITE` SDP body, look for:

```
a=rtpmap:101 telephone-event/8000
a=fmtp:101 0-15
```

This means RFC 2833 DTMF is negotiated on payload type `101`. If this line is absent, in-band or SIP INFO DTMF may be used instead.

#### RFC 2833 / RFC 4733 DTMF (most common)

DTMF tones sent as RTP events show up as separate RTP packets with the negotiated telephone-event payload type (commonly `101`).

Filter for them in Wireshark:

```
rtp.p_type == 101
```

Click any matching packet and expand **Real-Time Transport Protocol → RFC 2833 RTP Event**:

| Field          | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| `Event ID`     | Digit pressed: 0–9, `*`=10, `#`=11, A–D=12–15                      |
| `End of event` | `True` on the final packet for this digit                          |
| `Volume`       | Signal level in dBm0                                               |
| `Duration`     | Tone duration in RTP timestamp units (divide by clock rate for ms) |

#### SIP INFO DTMF (less common)

Some providers send DTMF as SIP INFO messages instead of RTP. Filter for them:

```
sip.Method == "INFO"
```

Expand the packet and look for a body like:

```
Signal=5
Duration=160
```

#### In-band DTMF (audio tones in RTP)

In-band DTMF is embedded in the audio stream as 350/440 Hz or 697–1633 Hz dual tones and cannot be filtered directly in Wireshark. To detect it:

1. Export the RTP audio as described in **Analyze RTP streams** above.
2. Analyze in Audacity (View → Spectrogram) or use a DTMF decoder library.

<Note>
  Retell captures RFC 2833 DTMF by default. Refer to [Capture DTMF input from user](/build/user-dtmf) for configuring DTMF completion options (digit limit, termination key, timeout).
</Note>

***

### Capture a PCAP file

If you don't already have a PCAP, capture one at the network level.

#### Option A: Capture with `tcpdump`

`tcpdump` is pre-installed on Linux and macOS. For other platforms, see [tcpdump.org](https://www.tcpdump.org/).

Capture all SIP (port 5060) and RTP (UDP ports 10000–20000) traffic on your network interface:

```bash theme={null}
sudo tcpdump -i eth0 -w call_capture.pcap \
  'udp port 5060 or (udp portrange 10000-20000)'
```

| Flag                        | Description                                                |
| --------------------------- | ---------------------------------------------------------- |
| `-i eth0`                   | Network interface to capture on (use `any` to capture all) |
| `-w call_capture.pcap`      | Output file                                                |
| `udp port 5060`             | SIP signaling traffic                                      |
| `udp portrange 10000-20000` | Typical RTP media port range                               |

Stop the capture with `Ctrl+C` once the call ends.

#### Option B: Capture with Wireshark (GUI)

1. Open Wireshark and select your network interface.
2. Set the capture filter: `udp port 5060 or udp portrange 10000-20000`
3. Click **Start** (blue shark fin icon).
4. Place and complete the test call.
5. Click **Stop**, then **File → Save As** to save as `.pcap` or `.pcapng`.

<Note>
  If you are using Retell with a custom SIP trunk, capture traffic on the server or gateway that terminates SIP — not your local machine. See [Custom Telephony](/deploy/custom-telephony) for Retell's SIP server IP ranges to filter for.
</Note>

***

### Analyze with `tshark` (CLI)

For scripting and server-side analysis without a GUI:

#### Extract all SIP messages

```bash theme={null}
tshark -r call_capture.pcap -Y sip -T fields \
  -e frame.time \
  -e ip.src \
  -e ip.dst \
  -e sip.Method \
  -e sip.Status-Code \
  -e sip.Call-ID
```

#### List all RTP streams with stats

```bash theme={null}
tshark -r call_capture.pcap -q -z rtp,streams
```

#### Extract RFC 2833 DTMF events

```bash theme={null}
tshark -r call_capture.pcap \
  -Y "rtp.p_type == 101" \
  -T fields \
  -e frame.time \
  -e ip.src \
  -e rtpevent.event_id \
  -e rtpevent.end_of_event
```

#### Export all RTP audio for a stream

```bash theme={null}
tshark -r call_capture.pcap \
  --export-objects rtp,/tmp/rtp_streams/
```

***

### Use `sngrep` for a quick terminal SIP view (optional)

`sngrep` provides a real-time or offline SIP ladder diagram in the terminal — no GUI needed.

```bash theme={null}
# Install
brew install sngrep        # macOS
sudo apt install sngrep    # Debian/Ubuntu

# Read from PCAP
sngrep -I call_capture.pcap

# Live capture on SIP port
sudo sngrep -d eth0 port 5060
```

Navigate with arrow keys to select a call, then press **Enter** to view its full SIP flow and raw message content.


# Debug outbound connection issues
Source: https://docs.retellai.com/reliability/debug-outbound-call

Diagnose outbound call disconnection reasons.

When an outbound call is made and the call has a status of `not_connected`, it means that the outbound call has not successfully established the connection to the destination number. There are a few reasons for this, and it is tracked in the `disconnection_reason` field of the call.

## Disconnection reasons for not connected calls

* `invalid_destination`: representing cases where the destination phone number is invalid. It could that there are spaces or invalid characters in the number. Or it can be your telephony provider requiring specific format (like e.164 format).
* `telephony_provider_permission_denied`: representing cases where the sip trunk authentication failed.
* `telephony_provider_unavailable`: representing cases where the telephony provider is not available or has errors.
* `sip_routing_error`: representing cases where there are loops or issues with the sip routing.
* `marked_as_spam`: representing cases where the call is marked as spam. Read more about root cause and remediation methods below.
* `user_declined`: representing cases where the user explicitly declined the call.
* `dial_failed`: representing cases where sip error codes are not available, or error is unknown.
* `dial_busy`: The number dialed is busy.
* `dial_no_answer`: The number dialed did not answer.

## Steps to troubleshoot

<Steps>
  <Step>
    Check the call history and detailed log. It contains the disconnection reason, the error message and optionally a **[SIP error code](/reliability/debug-calls-pcap#common-sip-response-code-reference)**. If the logs contain a SIP error then you can see the details by checking the PCAP file available in the call logs — see [Debug calls with PCAP](/reliability/debug-calls-pcap) for information on how to debug using PCAP files.
    In most cases, this would be enough for you to identify the root cause.

    <img />

    <Note>
      PCAP files are only available when the agent's data retention is set to **Everything** and the SIP transport is **UDP/TCP**. Calls using TLS transport or any other data retention setting will not have a PCAP available.
    </Note>
  </Step>

  <Step>
    If the call detailed log and PCAP file does not provide enough information, you can try the following:

    * If using custom telephony
      1. Double check your configuration and make sure you imported the right information. Refer to [FAQ](/deploy/custom-telephony#faq) for more info.
      2. If the configuration is not correct, delete the imported number and re-import.
      3. If that does not solve it, please check with your telephony provider to see what's the error on their side.

    * If using numbers purchased from Retell
      1. Make sure the destination number can accept the call. Currently, numbers purchased from Retell can only make calls to US numbers.
  </Step>
</Steps>

### Number marked as spam

When a number experiences high outbound call volume spike without any warmup, and/or has a low pickup rate, it might be marked as spam by carriers. When this happens, the number will get blocked frequently. To remedy this, you can try to:

* Purchase a new number, and warm it up before pouring all traffic to it (slowly add outbound traffic to it)
* Increase the pickup rate, read more at [Increase Pickup Rate](/build/telephony/call_efficiency_overview)
* Register the number with our spam remediation feature, read more at [verified phone number](/build/telephony/verified-phone)


# Fraud Protection
Source: https://docs.retellai.com/reliability/fraud-protection

Protect your Retell AI deployment with rate limiting and geographic restrictions

## Overview

Retell provides fraud protection features to help you prevent abuse of your voice AI agents. These features complement the general [abuse prevention measures](/reliability/prevent-abuse) and give you fine-grained control over how your agents are accessed.

## Rate Limiting

When using [public keys](/accounts/public-keys) to authenticate calls from your frontend, you can enable fraud protection to automatically rate limit requests based on IP address and destination phone number.

### Enabling Fraud Protection

You can enable fraud protection when creating or updating a public key:

1. Navigate to **Public Keys** in your Retell dashboard
2. Click on the public key you want to configure
3. Toggle on **Fraud Protection**
4. Save your changes

<Frame>
  <img alt="Public key settings with the fraud protection toggle enabled" />
</Frame>

### How It Works

When fraud protection is enabled on a public key:

* Requests are rate limited based on the combination of the caller's IP address and the destination phone number
* This prevents bad actors from using the same IP to spam calls to premium rate numbers
* The rate limiting applies to outbound phone calls and SMS initiated via public key authentication

<Tip>
  For maximum protection, combine fraud protection with [Google reCAPTCHA](/accounts/public-keys#google-recaptcha-v3-protection-optional) to prevent bot abuse.
</Tip>

## Geographic Restrictions

You can restrict which countries are allowed to make inbound calls to your Retell phone numbers, and which countries your phone numbers can make outbound calls to. This helps prevent International Revenue Sharing Fraud (IRSF) and limits your exposure to unwanted traffic.

### Allowed Inbound Countries

Restrict which countries can call your Retell phone numbers:

1. Navigate to **Phone Numbers** in your Retell dashboard
2. Click on the phone number you want to configure
3. Under **Allowed Inbound Countries**, add the countries that should be allowed to call this number

Changes are saved automatically.

<Frame>
  <img alt="Phone number settings showing the allowed inbound countries list" />
</Frame>

When configured, calls from countries not on the list will be automatically rejected.

### Allowed Outbound Countries

Restrict which countries your phone numbers can call:

1. Navigate to **Phone Numbers** in your Retell dashboard
2. Click on the phone number you want to configure
3. Under **Allowed Outbound Countries**, add the countries this number should be allowed to call

Changes are saved automatically.

<Frame>
  <img alt="Phone number settings showing the allowed outbound countries list" />
</Frame>

When configured, outbound calls to countries not on the list will be blocked.

### Configuring via API

You can also configure geographic restrictions via the [Update Phone Number API](/api-references/update-phone-number):

```bash theme={null}
curl -X PATCH "https://api.retellai.com/update-phone-number/+14155551234" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "allowed_inbound_country_list": ["US", "CA", "GB"],
    "allowed_outbound_country_list": ["US", "CA"]
  }'
```

Use [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country codes (e.g., "US" for United States, "CA" for Canada, "GB" for United Kingdom).

To remove restrictions, set the list to `null`:

```bash theme={null}
curl -X PATCH "https://api.retellai.com/update-phone-number/+14155551234" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "allowed_inbound_country_list": null,
    "allowed_outbound_country_list": null
  }'
```

### Sanctioned Countries

The following countries are always blocked regardless of your configuration:

| Country     | Code |
| ----------- | ---- |
| Cuba        | CU   |
| Iran        | IR   |
| North Korea | KP   |
| Syria       | SY   |
| Russia      | RU   |
| Belarus     | BY   |
| Venezuela   | VE   |

Calls to or from these countries will be automatically rejected.

## Best Practices

1. **Enable fraud protection on all public keys** - This adds an extra layer of protection against abuse at minimal cost
2. **Combine with reCAPTCHA** - Use both fraud protection and reCAPTCHA for web-initiated calls to prevent bot abuse
3. **Start with restrictive country lists** - Begin with only the countries you need and expand as necessary
4. **Monitor for blocked calls** - Use [webhooks](/features/webhook-overview) to track when calls are blocked due to geographic restrictions
5. **Review regularly** - Periodically review your country restrictions to ensure they match your current business needs


# Prevent abuse
Source: https://docs.retellai.com/reliability/prevent-abuse

Prevent bad actors from abusing your Retell AI agent.

## Abuse scenarios

Retell AI has implemented several mechanisms to prevent bad actors from using our agents to conduct malicious activities. However, there are cases where bad actors may pretend to be a customer and spam your agents.

Malicious activity usually comes in the form of International Revenue Sharing Fraud (IRSF). Bad actors are incentivized to do so because they get kickbacks from carriers when they direct traffic to them. Common abuse scenarios include:

* making excessive outbound calls, usually to non-US numbers, either via your phone call widget or form submission. They usually rotate the destination phone number, and use a real human recording to avoid being detected.
* making outbound SMS (even 2FA SMS) messages, usually to non-US numbers.
* making a large amount of unwanted inbound calls into a number that you made public. This is less common as it's usually not going to bring them kickbacks.
* using robots to spam your chat widget. This is less common as it's usually not going to bring them kickbacks.

## Abuse prevention

Here are a few high level rules of thumb to prevent abuse. We will dive into more details below:

1. Never expose your API key to the public; always use a [public key](/accounts/public-keys) in frontend.
2. If your API key is exposed, always rotate and revoke the key.
3. Always use a reCAPTCHA if possible to prevent bots from abusing your endpoints.
4. Only allow functionalities or regions that you need.
5. Implement rate limiting (number-based, IP-based, etc.) for your endpoints if necessary.
6. Have user identification mechanisms (KYC measures) in place if necessary.
7. Have a prompt in your agent that can potentially detect unrelated calls and hang up quickly.

### Protecting outbound calling / chatting capabilities

There are two ways that you can secure the calling / chatting capabilities that you expose to the public:

* have your own user access management system, and keep the Retell API calls to your backend only.
* use the [Retell widgets](/deploy/chat-widget) to embed the calling / chatting capabilities into your website. It's highly recommended to enable [reCAPTCHA](/accounts/public-keys#google-recaptcha-v3-protection-optional) to prevent bots from abusing your endpoints.

### Protecting inbound calling

When a number is made public, it's possible to have unwanted traffic. You can set up [inbound webhooks](/features/inbound-call-webhook) to detect and block unwanted traffic based on the incoming number.

### Advanced Protection

For additional fraud protection features including rate limiting by IP/phone number and geographic restrictions per phone number, see [Fraud Protection](/reliability/fraud-protection).


# Reliability Overview
Source: https://docs.retellai.com/reliability/reliability-overview

Discover how Retell AI ensures 99.9% uptime with enterprise-grade infrastructure, proactive monitoring, and fallback mechanisms. Learn about our reliability strategy, resilience features, and support system

At Retell, we've made reliability our **top priority**. Our platform is built on enterprise-grade infrastructure to ensure consistent, high-quality performance for all your voice AI needs.

We focus on three key areas to maintain exceptional service quality:

1. **Phone Call Performance**
   * Reliable handling of inbound and outbound calls
   * Consistent connection throughout conversations
   * High voice quality

2. **Agent Reliability**
   * Consistent low latency during interactions

3. **Agent Performance**
   * Accurate speech transcription
   * Strict adherence to prompt instructions

### Our Commitment to Reliability

At Retell, we guarantee **>99.9% uptime**. To achieve this, we've invested on the following areas:

1. **Enterprise-grade infrastructure**
2. **Fallbacks and Resilience Features**
3. **24/7 Monitoring and Alerting**
4. **24/7 Support**

### Detailed Overview

1. **Enterprise-grade infrastructure**: We conduct extensive load testing on high traffic and maintain dedicated auto-scaling and provisioning to handle varying loads. Our enterprise-grade compute, networking, and infrastructure ensure stable performance.
   * We guarantee **>99.9% uptime** - Subscribe to our [Status Page](https://status.retellai.com/) to get notified about any issues.
   <Frame>
     <img />
   </Frame>
   * Self-hosted models to reduce third-party dependencies.
   * **Stable server cluster** (enterprise only): Opt in to route both calls and API requests to our stable server cluster, which receives delayed feature rollouts for added production stability. When enabled, point your API requests to `https://stable.retellai.com/` instead of `https://api.retellai.com/`. A \$0.02/min surcharge applies on calls. Contact [support](/general/support) to enable.

2. **Proactive Monitoring**: We maintain 24/7 latency monitoring and alerting systems to catch and address issues before they impact your operations.
   * Including ASR, TTS, LLM, Knowledge base, time to first token, and network latency distribution, p75, p90, p95, p99 latencies.
   * Failed calls count, ASR, LLM, TTS timeout, and error rate.
   * Server CPU, GPU, memory, and network usage. Database, API response time.

3. **Resilience Features**: We've implemented fallbacks, retries, and other features to improve reliability:
   * [Branded Call/Verified Phone Number Features](/build/telephony/call_efficiency_overview) to improve call pickup rate and allowlist carrier calls
   * [TTS fallback and retries](/build/tts-fallback) is automatically built in, and can be manually configured.
   * LLM fallback and retries is automatically built in.

4. [Testing Features](/test/test-overview)

5. **Support System**: Our dedicated support team is ready to assist if any issues arise.
   * 7 days/week on-call schedule
   * 24h SLA, with active support between 9 AM to 9 PM PST (lower for enterprise customers)
     Read more about support [here](/general/support).


# Troubleshoot high latency
Source: https://docs.retellai.com/reliability/troubleshoot-latency

Follow these steps to resolve high end-to-end latency issues.

If your end-to-end latency P90 exceeds **3 seconds**, follow these troubleshooting steps.

<Steps>
  <Step title="Check Estimated Latency">
    1. Look for features marked with a turtle icon 🐢 in your configuration
    2. Check if your estimated latency is higher than 1.5s
    3. If high, disable some features to reduce latency

    <Frame>
      <img alt="Features that increase latency" />
    </Frame>
  </Step>

  <Step title="Monitor LLM Response Time">
    1. Check your current LLM latency
    2. Compare against normal range (500ms - 900ms)
    3. If consistently above 900ms:
       * Use [fast tier](/build/llm-options#fast-tier)
       * Switch to an alternative LLM provider
       * Or wait for your current provider to resolve performance issues
  </Step>

  <Step title="Check Status Page">
    1. Check the [Status Page](https://status.retellai.com/) for any ongoing issues
    2. If there are any ongoing issues, wait for them to resolve
  </Step>

  <Step title="Consider Geographic Distance">
    International phone calls may introduce additional latency due to geographic distance:

    1. Check if you're making calls between different countries or continents
    2. Consider getting a local phone number in the same region as your users
    3. Use phone numbers geographically closer to your target audience for better performance
  </Step>

  <Step title="Contact Support">
    If the above steps don't resolve your latency issues:

    1. Locate your call ID
    2. Message the [support](/general/support)
    3. Include:
       * Your call ID
       * Steps you've already tried
       * Current latency measurements
  </Step>
</Steps>


# Debug wrong response
Source: https://docs.retellai.com/reliability/wrong-response

How to fix when your AI agent gives incorrect responses

<Steps>
  <Step title="Check Model Capability">
    If your agent isn't following instructions correctly, especially with longer or complex prompts:

    1. Check if you're using a lightweight model (e.g., 4.1-mini)
    2. Switch to a more capable model like `gpt-4.1`

    <Frame>
      <img />
    </Frame>
  </Step>

  <Step title="Review Prompt Structure">
    If the issue persists:

    1. Check if your prompt structure is too complex
    2. Follow [prompt engineering guide](https://www.promptingguide.ai/)
    3. Break down complex tasks into clear, sequential steps
    4. Add explicit transition conditions between different steps
  </Step>
</Steps>


# Increase transcription accuracy
Source: https://docs.retellai.com/reliability/wrong-transcript



We take transcription quality seriously and understand its crucial importance for our customers. Our transcription accuracy primarily depends on the AI models we use, carefully selected to balance both accuracy and processing speed.

### Common Transcription Issues and Solutions

#### 1. Wrong Transcript for Special Words or Terms

**Issue**: Specific words (like "retell") or domain-specific terms (such as medical terminology) are missing from transcripts.

**Solution**: Use Boosted Keywords

* Add custom keywords to enhance the model's vocabulary
* Support for up to 100 custom keywords

<Frame>
  <img alt="Boosted Keywords Configuration" />
</Frame>

#### 2. Transcription error due to background noise / speech

Play with [denoising mode setting](/build/handle-background-noise) to see if it helps.

#### 2. Transcription error due to sentence being cut off

Sometimes the transcription quality can be impacted if the sentence was cut off (the transcription spits out the finalized sentence before it should). In this case, you can turn on [transcription mode](/build/transcription-mode) to be optimized for accuracy.

## FAQ

<AccordionGroup>
  <Accordion title="The agent is missing short responses like 'sure' or 'yes'. How do I fix this?">
    If the background noise level is not particularly high, this is often caused by the denoising mode filtering out short, low-energy responses. Try setting the [denoising mode](/build/handle-background-noise) to **No Denoising** — this preserves more of the raw audio signal and can significantly improve ASR accuracy for brief utterances when the environment is relatively quiet.
  </Accordion>
</AccordionGroup>


# Batch test your agent
Source: https://docs.retellai.com/test/batch-test-simulation



## Overview

When testing your agent, you may have multiple test cases to verify. Running them in batch can significantly save time and effort.

Additionally, since Language Models (LLMs) can sometimes produce inconsistent or unexpected results, running tests multiple times helps ensure more reliable and accurate outcomes.

## Steps

### Step 1: Navigate to the Simulation Tab

<Frame>
  <img alt="Simulation tab" />
</Frame>

### Step 2: Set Up Your Test Cases

You have two options for test cases:

* Use existing test cases
* Create new test cases

For creating new test cases, you can either do it here or in the LLM Simulation Testing page. For detailed instructions, see [LLM Simulation Testing](/test/llm-simulation-testing).

### Step 3: Define the parameters

<Frame>
  <img alt="Create test case" />
</Frame>

### Step 4: Execute the Tests

Choose the test cases you want to run from your test suite.

<Frame>
  <img alt="Run tests" />
</Frame>


# Manually test your agent
Source: https://docs.retellai.com/test/llm-playground

Learn how to effectively test and debug your AI agents using the LLM Playground

The LLM Playground provides a convenient environment for testing your AI agents without making actual web or phone calls. This interactive testing interface enables:

* Rapid prototyping and debugging of agent responses
* Testing different conversation scenarios
* Immediate feedback on agent behavior
* Faster development iterations

<Steps>
  <Step title="Access the LLM Playground">
    1. Navigate to your agent's detail page
    2. Click on the "Test LLM" tab
    3. Choose "Manual Chat".
    4. You'll see the chat interface where you can start testing

    <Frame>
      <img alt="Screenshot of the LLM Playground interface" />
    </Frame>
  </Step>

  <Step title="Test Basic Conversations">
    1. Type your message in the input field
    2. Observe the agent's response
  </Step>

  <Step title="Test Function Calling">
    1. Use prompts that should trigger specific functions
    2. Verify that functions are called with correct parameters

    <Frame>
      <img alt="Screenshot of the function calling test" />
    </Frame>
  </Step>

  <Step title="Iterate and Refine">
    1. Monitor agent behavior and responses
    2. Update prompts or functions as needed
    3. Click the "delete" button to reset conversations
    4. Test the updated behavior

    <Frame>
      <img alt="Screenshot of the iteration process" />
    </Frame>
  </Step>

  <Step title="Save Test Cases">
    1. Click the "Save" button to store your test conversation
    2. Add a descriptive name for the test case
    3. Access saved tests from the agent detail page

    <Frame>
      <img alt="Screenshot of saving a test case" />
    </Frame>

    <Frame>
      <img alt="Screenshot of saved test cases" />
    </Frame>
  </Step>

  <Step title="Test Dynamic Variables">
    1. Use dynamic variables in your prompts
    2. Verify that variables are properly interpolated
    3. Test different variable values and scenarios

    <Frame>
      <img alt="Screenshot of dynamic variables" />
    </Frame>
  </Step>

  <Step title="Mock Custom Function">
    Add a mock response for functions during testing. This response will be returned instead of making an actual function call, ensuring that no real execution occurs.

    <Frame>
      <img alt="Screenshot of custom function mock" />
    </Frame>
  </Step>
</Steps>

### Best Practices

* Start with simple conversations and gradually test more complex scenarios
* Save important test cases for regression testing
* Test edge cases and error handling
* Document unexpected behaviors for future reference


# Debug your agent response
Source: https://docs.retellai.com/test/llm-playground-debug



Here's how to troubleshoot common issues:

## When the agent's response is unexpected

Step 1: Click the "Debug" button on the agent's response

<Frame>
  <img alt="LLM Playground Debug" />
</Frame>

Step 2: Follow the suggested solutions

<Frame>
  <img alt="Suggested solutions for unexpected responses" />
</Frame>

Available solutions:

1. Add fine-tuning examples ([guide](/build/conversation-flow/debug-guide#add-conversation-finetune-examples))
2. Split the node into multiple nodes ([guide](/build/conversation-flow/debug-guide#split-the-node-into-multiple-nodes))
3. Adjust the LLM temperature ([guide](/build/conversation-flow/debug-guide#adjust-the-llm-temperature))

Step 3: Click "Regenerate Answer" to get a new response

Step 4: Use "Regenerate 10 Times" to test response consistency

## When the agent doesn't transition correctly

Step 1: Click the "Debug" button on the agent's response

<Frame>
  <img alt="LLM Playground Debug" />
</Frame>

Step 2: Click "Didn't transition as expected?"

Step 3: Follow the suggested solutions

<Frame>
  <img alt="Suggested solutions for incorrect transitions" />
</Frame>

Available solutions:

1. Add fine-tuning transition examples ([guide](/build/conversation-flow/debug-guide#add-transition-finetune-examples))
2. Split the node into multiple nodes ([guide](/build/conversation-flow/debug-guide#split-the-node-into-multiple-nodes))

Step 4: Click "Regenerate Transition" to get a new response

## When the agent transitions at the wrong time

Step 1: Click the "Debug" button on the transition dialog

<Frame>
  <img alt="Debug button on a wrong-time transition" />
</Frame>

Step 2: Follow the suggested solutions

<Frame>
  <img alt="Suggested solutions for incorrect transitions" />
</Frame>

Available solutions:

1. Add fine-tuning transition examples ([guide](/build/conversation-flow/debug-guide#add-transition-finetune-examples))
2. Split the node into multiple nodes ([guide](/build/conversation-flow/debug-guide#split-the-node-into-multiple-nodes))

Step 3: Click "Regenerate Transition" to get a new response

## When the agent's responses are inconsistent

Step 1: Click the "Debug" button on the agent's response

Step 2: Try these solutions:

1. Add fine-tuning examples ([guide](/build/conversation-flow/debug-guide#add-conversation-finetune-examples))
2. Split the node into multiple nodes ([guide](/build/conversation-flow/debug-guide#split-the-node-into-multiple-nodes))
3. Adjust the temperature ([guide](/build/conversation-flow/debug-guide#adjust-the-llm-temperature))

Step 3: Use "Regenerate 10 Times" to test response consistency

Step 4: Click "Regenerate 10 Times" to test response consistency

<Frame>
  <img alt="Regenerate 10 Times button for consistency testing" />
</Frame>


# Automatically test your agent
Source: https://docs.retellai.com/test/llm-simulation-testing



## Overview

You can create user prompts to guide how users would interact with your agent and evaluate the results using defined metrics.

## Steps

### Step 1: Create a new test case

Click "AI Simulated Chat" to create a new test case.

<Frame>
  <img alt="Create test case" />
</Frame>

### Step 2: Define the user prompt

Define the user scenario by providing a prompt. We recommend using this format:

```
## Identity

Your name is Mike.
Your date of birth is June 10, 1999.
Your order number is 7891273.

## Goal

Your primary objective is to return the package you received and get a refund.

## Personality

You are a patient customer. However, if the conversation becomes too long or complicated, you will show signs of impatience. If the issue remains unresolved, you may become frustrated and angry.
```

### Step 3: Select LLM Model

You can select which LLM model to use to generate user conversation.

### Step 4: Run the simulation

Click "Test" to start the conversation.

### Step 5: Review the results

Manually review the conversation to identify any issues.

### Step 6: Save as test case

Click "Save" to preserve the test case for future use.

<Frame>
  <img alt="Create test case" />
</Frame>

### Step 7: Define the evaluation metrics

Define the metrics you want to measure. We recommend using this format:

```
1. Verify that the customer successfully returned the package and received a refund.
2. Confirm that the end_call function was called at the end of the conversation.
3. Ensure the agent's responses are conversational and contain 5 sentences or fewer.
```

### Step 7: (Optional) Configure test variables and function mocks

You can specify dynamic variables to be used during testing.

Additionally, you can set up mocks for custom functions to prevent calling actual functions during testing, ensuring consistent results across test runs.


# Testing Overview
Source: https://docs.retellai.com/test/test-overview

Comprehensive testing methods to validate your AI agent's performance before production deployment

## Introduction

Thorough testing is crucial for building reliable AI phone agents. Retell provides multiple testing methods, each designed to validate different aspects of your agent's behavior and performance.

## Available Testing Methods

### 1. LLM Playground

**Purpose**: Interactive text-based testing for rapid iteration and debugging

**Key Features**:

* Real-time conversation testing
* Function call visualization
* Variable inspection
* Prompt debugging

<Frame>
  <img alt="LLM Playground interface showing conversation testing and function calls" />
</Frame>

**Best For**: Initial development, prompt refinement, debugging specific conversation paths

### 2. LLM Simulation Testing

**Purpose**: Automated testing with predefined scenarios for consistent quality assurance

**Key Features**:

* Batch testing capabilities
* Success metrics and scoring
* Scenario templates
* Regression testing

<Frame>
  <img alt="Simulation testing dashboard showing test scenarios and success metrics" />
</Frame>

**Best For**: Quality assurance, regression testing, validating changes before deployment

### 3. Web Call/Phone Call Testing

**Purpose**: Real-world testing with actual voice interactions to validate audio performance

**Key Features**:

* Test voice quality and latency
* Validate interruption handling
* Check background noise processing
* Verify DTMF and telephony features

<Frame>
  <img alt="Web call testing interface for making test calls to your agent" />
</Frame>

**Best For**: Final validation, voice quality testing, production readiness checks

## Testing Method Comparison

| Feature               |   LLM Playground  |   LLM Simulation  | Web/Phone Call | Audio Simulation |
| --------------------- | :---------------: | :---------------: | :------------: | :--------------: |
| **Availability**      |     All agents    |     All agents    |   All agents   |    Coming soon   |
| **Setup effort**      |       Medium      |        Low        |      High      |        Low       |
| **Test speed**        |        Fast       |     Very fast     |    Real-time   |       Fast       |
| **Response accuracy** |         ✅         |         ✅         |        ✅       |         ✅        |
| **Function calls**    |         ✅         |         ✅         |        ✅       |         ✅        |
| **Background noise**  |         ❌         |         ❌         |        ✅       |         ✅        |
| **Interruptions**     |         ❌         |         ❌         |        ✅       |         ✅        |
| **Batch testing**     |         ❌         |         ✅         |        ❌       |         ✅        |
| **Cost**              | Price per message | Price per message |  Call charges  |       Free       |

## Recommended Testing Workflow

### Phase 1: Development Testing

**Tool**: LLM Playground

* Iterate on prompts and conversation flows
* Debug function calling logic
* Test edge cases interactively
* Validate dynamic variables

### Phase 2: Quality Assurance

**Tool**: LLM Simulation Testing

* Create comprehensive test scenarios
* Run regression tests after changes
* Validate success metrics
* Ensure consistent performance

### Phase 3: Production Validation

**Tool**: Web/Phone Call Testing

* Test actual voice interactions
* Verify audio quality and latency
* Check telephony features
* Validate real-world performance

### Phase 4: Continuous Testing

**Tool**: Batch Testing (Simulation)

* Set up automated test suites
* Monitor agent performance over time
* Catch regressions early
* Maintain quality standards

<Tip>
  **Pro tip**: Create a test checklist covering all critical paths before each deployment. Include both happy paths and edge cases.
</Tip>


# Phone call testing
Source: https://docs.retellai.com/test/test-phone



You can purchase a Retell phone number and easily test your agent by making phone calls.

Check this [page](/deploy/purchase-number) for more details.


# Web call testing
Source: https://docs.retellai.com/test/test-web



In the agent detail page, click "Test" to make a web call to test your agent.

<Frame>
  <img alt="Testing web call" />
</Frame>

