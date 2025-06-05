# 🤖 AI-Driven Project Planning Prompt

<Purpose>
Since you are Augment Agent and understand your capabilities better than anyone else, I need your expertise to frame out the high-level direction, user stories, and implementation tasks for the given <Requirement> below. This will establish our commit-driven Agile workflow using a centralized project management approach with specialized AI agent roles.
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
        <Strategy>Single master Linear project with labels/tags for different features and repositories</Strategy>
        <Swimlanes>["Backlog", "Todo", "In Progress", "Blocked", "Code Review", "Done"]</Swimlanes>
        <InitialState>All issues start in "Backlog"</InitialState>
        <GroomingProcess>Weekly sessions to move items from Backlog to Todo/In Progress</GroomingProcess>
        <VelocityTracking>Track team velocity across all features and milestones in unified view</VelocityTracking>
    </Project>
    <IssueTracking>
        <Mapping>1 User Story = 1 Linear Issue</Mapping>
        <TaskTracking>Individual tasks tracked as sub-items or checklist items</TaskTracking>
        <CommitLinking>All commits reference Linear issue IDs for traceability</CommitLinking>
        <Labeling>Use labels for: feature-name, repository, priority, agent-role, tech-stack</Labeling>
        <MultiRepo>Support features spanning multiple existing and new repositories</MultiRepo>
    </IssueTracking>
</LinearIntegration>

<SpecializedAgentRoles>
    <DevOpsAgent>
        <Responsibilities>CI/CD pipelines, infrastructure, deployment, containerization, monitoring</Responsibilities>
        <Tools>Docker, GitHub Actions, pre-commit hooks, deployment scripts</Tools>
        <Handoff>Clear infrastructure requirements, deployment targets, scaling needs</Handoff>
    </DevOpsAgent>
    <FeatureAgent>
        <Responsibilities>Business logic, core functionality, API development, data models</Responsibilities>
        <Tools>Primary programming languages, frameworks, databases, APIs</Tools>
        <Handoff>Detailed functional requirements, API specifications, data schemas</Handoff>
    </FeatureAgent>
    <QAAgent>
        <Responsibilities>Test strategy, test implementation, validation, quality assurance</Responsibilities>
        <Tools>Testing frameworks, test data, validation tools, performance testing</Tools>
        <Handoff>Test scenarios, acceptance criteria, performance requirements</Handoff>
    </QAAgent>
    <DocumentationAgent>
        <Responsibilities>Technical docs, README files, API documentation, architectural diagrams</Responsibilities>
        <Tools>Markdown, Mermaid diagrams, API doc generators, wikis</Tools>
        <Handoff>Documentation standards, target audience, maintenance requirements</Handoff>
    </DocumentationAgent>
</SpecializedAgentRoles>

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
    <FinalThought>Specify which specialized agent role is best suited for each user story</FinalThought>
    <FinalThought>Support multi-repository features with clear repository targeting</FinalThought>
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

    <UserStoryTemplate>
        # 🎯 [Feature Name] - [Story Title]

        ## 🧩 Summary
        As a(n) **[Role]**, I need to **[Goal]**, so that **[Business/Technical Value]**.

        ## ✅ Context
        - **Repository**: [target-repo-name or "new repository"]
        - **Feature Label**: [feature-name]
        - **Dependencies**: [Other stories, services, or systems]
        - **Risk Level**: [Low | Medium | High]
        - **Priority**: [P0 | P1 | P2]
        - **Estimated Effort**: [S | M | L | XL]

        ## 🔧 Tasks
        - [ ] **Task 1**: [Actionable engineering task]
        - [ ] **Task 2**: [Actionable engineering task]
        - [ ] **Task 3**: [Actionable engineering task]

        ## 📌 Acceptance Criteria
        - [ ] **AC1**: [Specific, testable criterion]
        - [ ] **AC2**: [Specific, testable criterion]
        - [ ] **AC3**: [Specific, testable criterion]

        ## 📎 Implementation Notes
        - **Design Constraints**: [Standards, patterns, or architectural requirements]
        - **Security Considerations**: [Security, compliance, or data protection needs]
        - **Performance Requirements**: [Latency, throughput, or scalability needs]
        - **Integration Points**: [APIs, services, or systems to integrate with]

        ## 🤖 AI Agent Assignment
        - **Primary Agent**: [DevOps | Feature | QA | Documentation]
        - **Secondary Agents**: [List any supporting agent roles needed]
        - **Handoff Requirements**: [Specific context, access, or prerequisites needed]
        - **Success Validation**: [How the agent will know the work is complete]

        ## 🔗 Linear Integration
        - **Labels**: [feature-name, repository-name, agent-role, priority]
        - **Epic/Milestone**: [Parent epic or milestone this story contributes to]
        - **Commit Pattern**: `[type](scope): description - Refs: [LINEAR-ID]`
    </UserStoryTemplate>
</Variables>
