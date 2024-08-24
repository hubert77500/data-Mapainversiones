create table if not exists public.org
(
    id                  uuid                     default uuid_generate_v4() not null
        primary key,
    created_at          timestamp with time zone default now()              not null,
    name                text                                                not null,
    plan                org_plan                                            not null,
    play_allowance      integer                  default 3                  not null,
    stripe_customer     text,
    stripe_subscription text,
    limited             boolean                  default false              not null,
    plan_period         text                     default 'monthly'::text    not null,
    canceled            boolean                  default false              not null,
    saml_idp_xml        text,
    saml_enabled        boolean                  default false,
    radar_allowance     integer                  default 500,
    eval_allowance      integer                  default 500
);

create table if not exists public.account
(
    id               uuid                     default uuid_generate_v4() not null
        primary key,
    created_at       timestamp with time zone default now()              not null,
    email            text
        unique,
    password_hash    text,
    recovery_token   text,
    name             text,
    org_id           uuid
        references public.org
            on delete cascade,
    role             user_role                                           not null,
    verified         boolean                  default false              not null,
    avatar_url       text,
    last_login_at    timestamp with time zone,
    single_use_token text
);

create index if not exists account_org_id_idx
    on public.account (org_id);

create table if not exists public.project
(
    id         uuid                     default uuid_generate_v4() not null
        primary key,
    created_at timestamp with time zone default now()              not null,
    name       text                                                not null,
    org_id     uuid                                                not null
        references public.org
            on delete cascade
);


create table if not exists public.api_key
(
    id         serial
        primary key,
    created_at timestamp with time zone default now()              not null,
    type       api_key_type                                        not null,
    api_key    uuid                     default uuid_generate_v4() not null,
    project_id uuid                                                not null
        references public.project
            on delete cascade
);

create index if not exists api_key_project_id_idx
    on public.api_key (project_id);

create table if not exists public.external_user
(
    id          serial
        primary key,
    created_at  timestamp with time zone default now() not null,
    project_id  uuid                                   not null
        references public.project
            on delete cascade,
    external_id varchar,
    last_seen   timestamp with time zone,
    props       jsonb
);

create unique index if not exists external_user_project_id_external_id_idx
    on public.external_user (project_id, external_id);

create index if not exists external_user_lower_idx
    on public.external_user using gin (lower(props::text) public.gin_trgm_ops);

create index if not exists external_user_lower_idx1
    on public.external_user using gin (lower(external_id::text) public.gin_trgm_ops);

create index if not exists external_user_project_id_last_seen_idx
    on public.external_user (project_id asc, last_seen desc);

create index if not exists project_org_id_idx
    on public.project (org_id);

create table if not exists public.run
(
    id                  uuid                     default uuid_generate_v4() not null
        primary key,
    created_at          timestamp with time zone default now()              not null,
    ended_at            timestamp with time zone,
    duration            interval generated always as ((ended_at - created_at)) stored,
    tags                text[],
    project_id          uuid                                                not null
        references public.project
            on delete cascade,
    status              text,
    name                text,
    error               jsonb,
    input               jsonb,
    output              jsonb,
    params              jsonb,
    type                text                                                not null,
    parent_run_id       uuid
                                                                            references public.run
                                                                                on update cascade on delete set null,
    prompt_tokens       integer,
    completion_tokens   integer,
    cost                double precision,
    external_user_id    bigint
                                                                            references public.external_user
                                                                                on update cascade on delete set null,
    feedback            jsonb,
    is_public           boolean                  default false              not null,
    sibling_run_id      uuid
                                                                            references public.run
                                                                                on update cascade on delete set null,
    template_version_id integer,
    input_text          text generated always as ((input)::text) stored,
    output_text         text generated always as ((output)::text) stored,
    error_text          text generated always as ((error)::text) stored,
    runtime             text,
    metadata            jsonb
);

create table if not exists public.log
(
    id         bigint                                 not null
        primary key,
    created_at timestamp with time zone default now() not null,
    message    text,
    level      text,
    extra      jsonb,
    project_id uuid                                   not null
        references public.project,
    run_id     uuid
        references public.run
            on update cascade on delete cascade
);

create index if not exists run_type_parent_run_id_idx
    on public.run (type, parent_run_id);

create index if not exists run_type_idx
    on public.run (type);

create index if not exists run_duration_idx
    on public.run (duration);

create index if not exists run_lower_idx
    on public.run using gin (lower(name) public.gin_trgm_ops);

create index if not exists run_lower_idx1
    on public.run using gin (lower(output_text) public.gin_trgm_ops);

create index if not exists run_lower_idx2
    on public.run using gin (lower(input_text) public.gin_trgm_ops);

create index if not exists run_ended_at_created_at_idx
    on public.run (ended_at, created_at);

create index if not exists run_created_at_idx
    on public.run (created_at desc);

create index if not exists run_created_at_idx1
    on public.run (created_at);

create index if not exists run_created_at_project_id_idx
    on public.run (created_at, project_id);

create index if not exists run_project_id_external_user_id_idx
    on public.run (project_id, external_user_id);

create index if not exists run_project_id_type_idx
    on public.run (project_id, type);

create index if not exists run_project_id_type_created_at_idx
    on public.run (project_id asc, type asc, created_at desc);

create index if not exists run_project_id_idx
    on public.run (project_id);

create index if not exists run_external_user_id_idx
    on public.run (external_user_id);

create index if not exists run_tags_idx
    on public.run using gin (tags);

create index if not exists run_parent_run_id_idx
    on public.run (parent_run_id);

create index if not exists run_type_external_user_id_idx
    on public.run (type, external_user_id);

create index if not exists run_name_idx
    on public.run (name);

create index if not exists run_feedback_idx
    on public.run using gin (feedback);

create index if not exists run_metadata_idx
    on public.run using gin (metadata);

create index if not exists idx_run_id_parent_run_id
    on public.run (id, parent_run_id);

create index if not exists idx_run_feedback_null
    on public.run (id, parent_run_id)
    where (feedback IS NULL);

create index if not exists idx_run_parent_run_id_feedback
    on public.run (parent_run_id, feedback);

create index if not exists idx_run_id_parent_run_id_feedback
    on public.run (id, parent_run_id, feedback);

create table if not exists public.template
(
    id         serial
        primary key,
    created_at timestamp with time zone default now(),
    owner_id   uuid
                    references public.account
                        on delete set null,
    name       text,
    "group"    text,
    slug       text,
    project_id uuid not null
        references public.project
            on delete cascade,
    mode       text
);

create table if not exists public.template_version
(
    id          serial
        primary key,
    created_at  timestamp with time zone default now() not null,
    extra       jsonb,
    content     jsonb,
    template_id integer                                not null
        references public.template
            on delete cascade,
    version     integer,
    test_values jsonb,
    is_draft    boolean
);

create table if not exists public.radar
(
    id          uuid                     default uuid_generate_v4() not null
        primary key,
    description text,
    project_id  uuid                                                not null
        references public.project
            on delete cascade,
    owner_id    uuid
                                                                    references public.account
                                                                        on delete set null,
    view        jsonb,
    checks      jsonb                                               not null,
    alerts      jsonb,
    negative    boolean,
    created_at  timestamp with time zone default now()              not null,
    updated_at  timestamp with time zone default now()              not null
);


create table if not exists public.radar_result
(
    id         uuid                     default uuid_generate_v4() not null
        primary key,
    radar_id   uuid                                                not null
        references public.radar
            on delete cascade,
    run_id     uuid
        references public.run
            on update cascade on delete cascade,
    created_at timestamp with time zone default now()              not null,
    results    jsonb[],
    passed     boolean,
    details    jsonb
);

create index if not exists radar_result_radar_id_run_id_idx
    on public.radar_result (radar_id, run_id);

create table if not exists public.checklist
(
    id         uuid                     default uuid_generate_v4() not null
        primary key,
    slug       text                                                not null,
    data       jsonb                                               not null,
    type       text                                                not null,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now(),
    owner_id   uuid
                                                                   references public.account
                                                                       on delete set null,
    project_id uuid                                                not null
        constraint fk_checklist_project_id
            references public.project
            on delete cascade
);


create table if not exists public.dataset
(
    id         uuid                     default uuid_generate_v4()        not null
        primary key,
    created_at timestamp with time zone default now()                     not null,
    updated_at timestamp with time zone default now()                     not null,
    project_id uuid                                                       not null
        references public.project
            on delete cascade,
    owner_id   uuid
                                                                          references public.account
                                                                              on delete set null,
    slug       text                                                       not null,
    format     varchar                  default 'chat'::character varying not null
);

create index if not exists dataset_project_id_slug_idx
    on public.dataset (project_id, slug);

create table if not exists public.evaluation
(
    id           uuid                     default uuid_generate_v4() not null
        primary key,
    created_at   timestamp with time zone default now()              not null,
    name         text                                                not null,
    project_id   uuid                                                not null
        references public.project
            on delete cascade,
    owner_id     uuid
                                                                     references public.account
                                                                         on delete set null,
    dataset_id   uuid
                                                                     references public.dataset
                                                                         on delete set null,
    models       text[]                                              not null,
    checks       jsonb                                               not null,
    providers    jsonb,
    checklist_id uuid
                                                                     references public.checklist
                                                                         on delete set null
);


create index if not exists evaluation_project_id_idx
    on public.evaluation (project_id);

create table if not exists public.dataset_prompt
(
    id         uuid                     default uuid_generate_v4() not null
        primary key,
    created_at timestamp with time zone default now()              not null,
    dataset_id uuid                                                not null
        references public.dataset
            on delete cascade,
    messages   jsonb                                               not null
);

create index if not exists dataset_prompt_dataset_id_idx
    on public.dataset_prompt (dataset_id);

create table if not exists public.dataset_prompt_variation
(
    id           uuid                     default uuid_generate_v4() not null
        primary key,
    created_at   timestamp with time zone default now()              not null,
    variables    jsonb                                               not null,
    context      text,
    ideal_output text,
    prompt_id    uuid                                                not null
        references public.dataset_prompt
            on delete cascade
);


create table if not exists public.evaluation_result
(
    id                uuid                     default uuid_generate_v4() not null
        primary key,
    evaluation_id     uuid                                                not null
        constraint fk_evaluation_result_evaluation_id
            references public.evaluation
            on delete cascade,
    prompt_id         uuid
        constraint fk_evaluation_result_prompt_id
            references public.dataset_prompt
            on delete cascade,
    variation_id      uuid
        constraint fk_evaluation_result_variation_id
            references public.dataset_prompt_variation
            on delete cascade,
    model             text,
    output            jsonb,
    results           jsonb,
    passed            boolean                  default false,
    completion_tokens integer,
    cost              double precision,
    duration          text,
    created_at        timestamp with time zone default now()              not null,
    provider          jsonb,
    status            text                     default 'success'::text    not null,
    error             text
);

create index if not exists dataset_prompt_variation_prompt_id_idx
    on public.dataset_prompt_variation (prompt_id);

create table if not exists public.account_project
(
    account_id uuid not null
        references public.account
            on delete cascade,
    project_id uuid not null
        references public.project
            on delete cascade,
    primary key (account_id, project_id)
);


