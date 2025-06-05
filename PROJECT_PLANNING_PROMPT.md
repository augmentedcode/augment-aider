# 🤖 AI-Driven Project Planning Prompt

<Purpose>
Since you are Augment Agent and understand your capabilities better than anyone else, I need your expertise to frame out the high-level direction, user stories, and implementation tasks for the given <Requirement> below. This will establish our commit-driven Agile workflow.
</Purpose>

<Objectives>
    <Objective>Collaborate to create a comprehensive project plan including technical architecture, user stories, and sequential tasks</Objective>
    <Objective>Ensure alignment between requirements, tech stack, and implementation approach</Objective>
    <Objective>Generate all necessary project artifacts for Linear PMS integration</Objective>
    <Objective>Establish DevOps automation pipeline configurations</Objective>
</Objectives>

<Workflow>
    <Step>Requirements Analysis & Tech Stack Validation</Step>
    <Step>Architecture Design & Component Planning</Step>
    <Step>User Story Creation with AI Agent Handoff Specifications</Step>
    <Step>Task Breakdown with Dependencies & Sequencing</Step>
    <Step>DevOps Pipeline Configuration Generation</Step>
    <Step>Linear Project Structure Definition</Step>
</Workflow>

<Considerations>
    <Consider>Analyze the provided <Requirement> and <TechStack> for technical feasibility and alignment</Consider>
    <Consider>Research current best practices and documentation for the proposed <TechStack> components</Consider>
    <Consider>Identify potential technical risks, dependencies, and integration challenges</Consider>
    <Consider>Suggest additional tools/frameworks that would enhance the <TechStack></Consider>
    <Consider>Design for testability, maintainability, and scalability from the start</Consider>
    <Consider>Ensure each user story can be independently implemented and tested</Consider>
    <Consider>Create tasks that provide clear success criteria and validation steps</Consider>
    <Consider>Generate comprehensive DevOps configurations for the full CI/CD lifecycle</Consider>
</Considerations>

<OutputRequirements>
    <File name="PLANNING.md">High-level project direction, scope, architecture, and success criteria</File>
    <File name="USERSTORIES.md">Detailed user stories in AI-agent-ready format with handoff specifications</File>
    <File name="TASKS.md">Sequential task breakdown with dependencies and validation criteria</File>
    <File name="ARCHITECTURE.mermaid">System architecture diagram showing components and data flow</File>
    <File name="TASK_FLOW.mermaid">Task dependency DAG for project execution planning</File>
    <File name=".pre-commit-config.yaml">Local CI pipeline with quality gates</File>
    <File name=".github/workflows/ci.yaml">Pull request validation pipeline</File>
    <File name=".github/workflows/cd.yaml">Main branch deployment pipeline</File>
    <File name=".github/workflows/release.yaml">Release artifact generation pipeline</File>
</OutputRequirements>

<LinearIntegration>
    <Project>
        <Swimlanes>["Backlog", "Todo", "In Progress", "Blocked", "Code Review", "Done"]</Swimlanes>
        <InitialState>All issues start in "Backlog"</InitialState>
        <GroomingProcess>Weekly sessions to move items from Backlog to Todo/In Progress</GroomingProcess>
    </Project>
    <IssueTracking>
        <Mapping>1 User Story = 1 Linear Issue</Mapping>
        <TaskTracking>Individual tasks tracked as sub-items or checklist items</TaskTracking>
        <CommitLinking>All commits reference Linear issue IDs for traceability</CommitLinking>
    </IssueTracking>
</LinearIntegration>

<QualityGates>
    <PreCommit>Code formatting, linting, type checking, unit tests</PreCommit>
    <PullRequest>All pre-commit checks + integration tests + security scans</PullRequest>
    <MainBranch>Full test suite + build validation + deployment readiness</MainBranch>
    <Release>Artifact generation + tagging + distribution + documentation</Release>
</QualityGates>

<FinalThoughts>
    <FinalThought>This is a collaborative dialog - ask follow-up questions one at a time for clarity</FinalThought>
    <FinalThought>You are a trusted technical partner, not just a tool</FinalThought>
    <FinalThought>Prioritize practical implementation over theoretical perfection</FinalThought>
    <FinalThought>Design for AI agent handoff - clear, actionable, and self-contained tasks</FinalThought>
    <FinalThought>Each task group should map 1:1 with a user story</FinalThought>
    <FinalThought>Include empty checkboxes for all tasks and acceptance criteria</FinalThought>
    <FinalThought>Use commit-driven feedback loops to inform next steps</FinalThought>
</FinalThoughts>

<Variables>
    <!-- These will be populated during the planning session -->
    <Requirement>
        <Feature>[To be provided]</Feature>
        <Description>[To be provided]</Description>
        <Summary>[To be provided]</Summary>
        <FunctionalRequirements>[To be provided]</FunctionalRequirements>
        <AcceptanceCriteria>[To be provided]</AcceptanceCriteria>
    </Requirement>
    <TechStack>[To be provided]</TechStack>
</Variables>
