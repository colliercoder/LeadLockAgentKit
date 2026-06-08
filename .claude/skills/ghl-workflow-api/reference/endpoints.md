# GHL private API endpoints

All paths are relative to the backend host unless noted.

- Base host: `https://backend.leadconnectorhq.com` (workflows, pipelines, emails)
- Webhook host: `https://services.leadconnectorhq.com` (inbound webhooks; not
  used by this skill)

Send the captured auth headers on every request (see `token-capture.md`).
Some endpoints additionally require a `version: 2021-07-28` header, noted below.

> Unofficial API. Shapes can change. Tokens expire ~hourly.

## Read

### List workflows
```
GET /workflow/{locationId}
```
Returns the location's workflows. Response is either a list or
`{"workflows": [...]}`. Each item has `id`, `name`, `status`.

### Workflow meta (gives you the signed file URL)
```
GET /workflow/{locationId}/{workflowId}
```
Returns meta for one workflow. The body has (under `workflow` or at the top
level) a `version` integer and a signed `fileUrl`. You need both: `version`
for writes, `fileUrl` to fetch the actual node JSON.

### Workflow node JSON (the actual flow)
```
GET <fileUrl>
```
`fileUrl` is a Firebase-signed URL. **Fetch it WITHOUT a `content-type`
header** or the signature breaks. The node list is at
`workflowData.templates` (or `templates` at the top level on older shapes).

### Pipelines and stages
```
GET /opportunities/pipelines?locationId={locationId}
header: version: 2021-07-28
```
Returns `{"pipelines": [{id, name, stages: [{id, name}, ...]}, ...]}`. Use
these ids to validate `create_opportunity` nodes.

### Email template library
```
GET /emails/builder?locationId={locationId}&limit=200
GET /emails/builder?locationId={locationId}&parentId={folderId}&limit=200
header: version: 2021-07-28
```
Returns `{"builders": [...]}`. Items with `templateType == "folder"` are
folders: re-query with `parentId` to get their contents. Non-folder items are
templates (their `id` is what an `email` node's `template_id` points at).

### Custom values / custom fields / tags
These follow the same location-scoped REST pattern. The general shape:
```
GET    /<resource>/?locationId={loc}        list
POST   /<resource>/                         create  (body includes locationId)
PUT    /<resource>/{id}                     update
DELETE /<resource>/{id}                     delete
```
Confirm the exact resource path for your need by watching the Network tab in
the builder while you perform the action once. Common resources: custom
values, custom fields, tags.

## Write

See `write-recipe.md` for the full version-pinning rules and bodies.

### Draft save
```
PUT /workflow/{locationId}/{workflowId}/auto-save
body: { templates, version }   # version = CURRENT version
```

### Publish
```
PUT /workflow/{locationId}/{workflowId}
body: { templates, version, status: "published", autoSaveSession: null }
```

## What you cannot do here

Triggers. GHL moved triggers to a separate "trigger bucket"
(`isTriggerBucketMigrated=true`); `newTriggers` / `oldTriggers` come back null,
so triggers and inbound-webhook trigger URLs must be set in the builder UI.
See `trigger-bucket-limitation.md`.
