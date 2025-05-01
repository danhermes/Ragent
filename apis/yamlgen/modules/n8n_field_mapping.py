# /ragents/projects/yamlgen/modules/n8n_field_mapping.py

# Defines the expected mapping between internal Piper fields and Markdown headings
TEMPLATE_FIELDS_N8N = {
    "workflow_name": "Workflow Name",
    "purpose_goal": "Purpose / Goal",
    "workflow_overview": "Workflow Overview",
    "trigger_node": "Trigger",
    "inputs": "Inputs",
    "outputs": "Outputs",
    "apps_services_apis": "Apps, Services, APIs",
    "nodes": "Nodes {node_name, node_type, description, params}",
    "connections": "Connections {source_node, target_node}",
    "workflow_settings": "Workflow Settings {key, value}",
    "test_scenarios": "Test Scenarios {condition, expected_result}",
    "authentication_permissions": "Authentication & Permissions",
    "completion_checklist": "Completion Checklist",
    "example_node_layout": "Example Node Layout {node1, node2, node3}"
}
