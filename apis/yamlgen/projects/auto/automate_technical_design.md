# 🧠 Technical Design – n8n Workflow Project

---

## 📛 Workflow Name
Dropbox Daily File Processor

---

## 🎯 Purpose / Goal
Scan a specific Dropbox folder daily and send a summary email listing all new PDF files.

---

## 🧩 Workflow Overview
Triggered every morning, the workflow will connect to Dropbox, list files in a target folder, filter for PDFs, and email a summary of file names to a recipient.

---

## 📥 Trigger
scheduleTrigger

---

## 📂 Inputs
- Daily scheduled time (6 AM)
- Dropbox folder path: `/DailyReports/`

---

## 📤 Outputs
- Email notification listing newly found PDF files.

---

## 🔗 Apps, Services, APIs
- Dropbox API
- SMTP Email Service

---

## 🧠 Core Nodes
- Schedule Trigger: scheduleTrigger - Activates daily at 6 AM.
- Dropbox List Files: dropboxList - Lists files from `/DailyReports/`.
- Filter Files: filter - Filters for `.pdf` files only.
- Email Sender: emailSend - Sends an email listing the filtered files.

---

## 🔄 Connections
- Schedule Trigger ➔ Dropbox List Files
- Dropbox List Files ➔ Filter Files
- Filter Files ➔ Email Sender

---

## 🛠 Workflow Settings (Optional)
- Timezone: America/New_York
- Save successful executions: true

---

## 🧪 Test Scenarios
1. Folder contains 5 PDFs ➔ Email lists 5 file names.
2. Folder is empty ➔ Email states \"No files found today.\"
3. Dropbox API call fails ➔ Error is logged and workflow stops.

---

## 🔒 Authentication & Permissions
- Dropbox: Dropbox OAuth2 API
- SMTP Email: SMTP Credentials

---

## ✅ Completion Checklist
- [ ] Workflow triggers reliably every morning.
- [ ] Only `.pdf` files are selected and listed.
- [ ] Summary email is formatted and sent successfully.
- [ ] API errors are logged correctly.
- [ ] Stakeholder approval obtained after successful tests.

---

## 📄 Example Node Layout (Optional Appendix)
- Schedule Trigger ➔ Dropbox List Files ➔ Filter Files ➔ Email Sender

---
