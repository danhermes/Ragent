Technical Specification:
  Create a Dropbox daily file processor using n8n.

workflow:
  name: Dropbox Daily File Processor
  settings:
    key: Save successful executions
    value: true
    timezone: UTC
nodes:
- node_name: Schedule Trigger
  node_type: scheduleTrigger
  description: Activates daily at 6 AM.
- node_name: Dropbox List Files
  node_type: dropboxList
  description: Lists files from `/DailyReports/`.
- node_name: Filter Files
  node_type: filter
  description: Filters for `.pdf` files only.
- node_name: Email Sender
  node_type: emailSend
  description: Sends an email listing the filtered files.
- node_name: Check Empty Folder
  node_type: emptyCheck
  description: Verifies if the folder is empty.
- node_name: Error Handler
  node_type: errorHandler
  description: Handles API errors and logs them.
connections:
- source_node: Schedule Trigger
  target_node: Dropbox List Files
- source_node: Dropbox List Files
  target_node: Filter Files
- source_node: Filter Files
  target_node: Check Empty Folder
- source_node: Check Empty Folder
  target_node: Email Sender
- source_node: Dropbox List Files
  target_node: Error Handler
