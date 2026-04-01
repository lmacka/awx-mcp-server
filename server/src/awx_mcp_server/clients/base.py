"""Base AWX client interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from awx_mcp_server.domain import (
    Inventory, Job, JobEvent, JobTemplate, Project,
    WorkflowJob, WorkflowJobTemplate, WorkflowNode,
)


class AWXClient(ABC):
    """Abstract base class for AWX clients."""

    @abstractmethod
    async def test_connection(self) -> bool:
        """
        Test connection to AWX.

        Returns:
            True if connection successful
        """
        pass

    @abstractmethod
    async def list_job_templates(
        self, name_filter: Optional[str] = None, page: int = 1, page_size: int = 25
    ) -> list[JobTemplate]:
        """List job templates."""
        pass

    @abstractmethod
    async def get_job_template(self, template_id: int) -> JobTemplate:
        """Get job template by ID."""
        pass

    @abstractmethod
    async def list_projects(
        self, name_filter: Optional[str] = None, page: int = 1, page_size: int = 25
    ) -> list[Project]:
        """List projects."""
        pass

    @abstractmethod
    async def get_project(self, project_id: int) -> Project:
        """Get project by ID."""
        pass

    @abstractmethod
    async def update_project(self, project_id: int, wait: bool = True) -> dict[str, Any]:
        """Update project from SCM."""
        pass

    @abstractmethod
    async def list_inventories(
        self, name_filter: Optional[str] = None, page: int = 1, page_size: int = 25
    ) -> list[Inventory]:
        """List inventories."""
        pass

    @abstractmethod
    async def launch_job(
        self,
        template_id: int,
        extra_vars: Optional[dict[str, Any]] = None,
        limit: Optional[str] = None,
        tags: Optional[list[str]] = None,
        skip_tags: Optional[list[str]] = None,
    ) -> Job:
        """Launch job from template."""
        pass

    @abstractmethod
    async def get_job(self, job_id: int) -> Job:
        """Get job by ID."""
        pass

    @abstractmethod
    async def list_jobs(
        self,
        status: Optional[str] = None,
        created_after: Optional[str] = None,
        page: int = 1,
        page_size: int = 25,
    ) -> list[Job]:
        """List jobs."""
        pass

    @abstractmethod
    async def cancel_job(self, job_id: int) -> dict[str, Any]:
        """Cancel running job."""
        pass

    @abstractmethod
    async def get_job_stdout(
        self, job_id: int, format: str = "txt", tail_lines: Optional[int] = None
    ) -> str:
        """Get job stdout."""
        pass

    @abstractmethod
    async def get_job_events(
        self, job_id: int, failed_only: bool = False, page: int = 1, page_size: int = 100
    ) -> list[JobEvent]:
        """Get job events."""
        pass

    # Workflow Job Templates

    @abstractmethod
    async def list_workflow_job_templates(
        self, name_filter: Optional[str] = None, page: int = 1, page_size: int = 25
    ) -> list[WorkflowJobTemplate]:
        """List workflow job templates."""
        pass

    @abstractmethod
    async def get_workflow_job_template(self, template_id: int) -> WorkflowJobTemplate:
        """Get workflow job template by ID."""
        pass

    @abstractmethod
    async def get_workflow_job_template_nodes(self, template_id: int) -> list[WorkflowNode]:
        """Get workflow job template nodes (DAG)."""
        pass

    @abstractmethod
    async def get_workflow_job_template_survey(self, template_id: int) -> dict[str, Any]:
        """Get workflow job template survey spec."""
        pass

    @abstractmethod
    async def get_workflow_job_template_launch_info(self, template_id: int) -> dict[str, Any]:
        """Get workflow job template launch requirements."""
        pass

    # Workflow Jobs

    @abstractmethod
    async def list_workflow_jobs(
        self, template_id: Optional[int] = None, status: Optional[str] = None,
        page: int = 1, page_size: int = 25,
    ) -> list[WorkflowJob]:
        """List workflow jobs."""
        pass

    @abstractmethod
    async def get_workflow_job(self, job_id: int) -> WorkflowJob:
        """Get workflow job by ID."""
        pass

    @abstractmethod
    async def get_workflow_job_nodes(self, job_id: int) -> list[WorkflowNode]:
        """Get workflow job nodes (runtime state)."""
        pass

    @abstractmethod
    async def launch_workflow(
        self, template_id: int, extra_vars: Optional[dict[str, Any]] = None,
        limit: Optional[str] = None, inventory: Optional[int] = None,
    ) -> WorkflowJob:
        """Launch workflow job template."""
        pass

    @abstractmethod
    async def cancel_workflow_job(self, job_id: int) -> dict[str, Any]:
        """Cancel running workflow job."""
        pass

    @abstractmethod
    async def relaunch_workflow_job(self, job_id: int) -> WorkflowJob:
        """Relaunch a workflow job."""
        pass

    @abstractmethod
    async def search_unified_job_templates(
        self, query: str, page_size: int = 25
    ) -> list[dict[str, Any]]:
        """Search across all template types."""
        pass

    # Workflow template management

    @abstractmethod
    async def copy_workflow_job_template(
        self, template_id: int, name: str
    ) -> WorkflowJobTemplate:
        """Copy a workflow job template."""
        pass

    @abstractmethod
    async def delete_workflow_job_template(self, template_id: int) -> None:
        """Delete a workflow job template."""
        pass

    # Workflow node CRUD

    @abstractmethod
    async def create_workflow_node(
        self, workflow_template_id: int, unified_job_template_id: int,
        limit: Optional[str] = None, extra_data: Optional[dict[str, Any]] = None,
        inventory: Optional[int] = None, all_parents_must_converge: bool = False,
    ) -> WorkflowNode:
        """Create a workflow node."""
        pass

    @abstractmethod
    async def update_workflow_node(
        self, node_id: int, limit: Optional[str] = None,
        extra_data: Optional[dict[str, Any]] = None,
        inventory: Optional[int] = None,
        all_parents_must_converge: Optional[bool] = None,
    ) -> WorkflowNode:
        """Update a workflow node."""
        pass

    @abstractmethod
    async def delete_workflow_node(self, node_id: int) -> None:
        """Delete a workflow node."""
        pass

    @abstractmethod
    async def add_workflow_node_edge(
        self, node_id: int, target_node_id: int, edge_type: str
    ) -> None:
        """Add an edge between workflow nodes."""
        pass

    @abstractmethod
    async def remove_workflow_node_edge(
        self, node_id: int, target_node_id: int, edge_type: str
    ) -> None:
        """Remove an edge between workflow nodes."""
        pass
