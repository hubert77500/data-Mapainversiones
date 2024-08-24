import AgentSummary from "@/components/analytics/AgentSummary"
import AnalyticsCard from "@/components/analytics/AnalyticsCard"
import BarList from "@/components/analytics/BarList"
import LineChart from "@/components/analytics/LineChart"
import UsageSummary from "@/components/analytics/UsageSummary"
import { formatAppUser, formatCost } from "@/utils/format"

import AppUserAvatar from "@/components/blocks/AppUserAvatar"
import Empty from "@/components/layout/Empty"
import {
  useAppUsers,
  useOrg,
  useProject,
  useRunsUsage,
  useRunsUsageByDay,
} from "@/utils/dataHooks"
import {
  Center,
  Container,
  Group,
  Loader,
  SegmentedControl,
  SimpleGrid,
  Stack,
  Title,
} from "@mantine/core"
import { useLocalStorage } from "@mantine/hooks"
import { IconChartAreaLine } from "@tabler/icons-react"
import { NextSeo } from "next-seo"

const calculateDailyCost = (usage) => {
  // calculate using calcRunCost, reduce by model, and filter by type llm
  // reduce by day

  const cost = usage.reduce((acc, curr) => {
    const { date, cost } = curr

    if (!acc[date]) acc[date] = 0
    acc[date] += cost

    return acc
  }, {})

  const final = Object.keys(cost).map((date) => ({
    date,
    cost: cost[date],
  }))

  return final
}

export default function Analytics() {
  const [range, setRange] = useLocalStorage({
    key: "dateRange-analytics",
    defaultValue: 7,
  })

  const { project } = useProject()
  const { org } = useOrg()

  const { usage, loading: usageLoading } = useRunsUsage(range)

  const { dailyUsage, loading: dailyUsageLoading } = useRunsUsageByDay(range)
  const { users, loading: usersLoading } = useAppUsers(range)

  const loading = usageLoading || dailyUsageLoading || usersLoading

  if (loading)
    return (
      <Center h="60vh">
        <Loader />
      </Center>
    )

  return (
    <Empty
      Icon={IconChartAreaLine}
      title="Waiting for data..."
      description="Analytics will appear here once you have some data."
      showProjectId
      enable={!loading && !project?.activated}
    >
      <Container size="lg" my="lg">
        <NextSeo title="Analytics" />
        <Stack gap="lg">
          <Group justify="space-between">
            <Title order={2}>Analytics</Title>
            <SegmentedControl
              w={300}
              value={range.toString()}
              onChange={(val) => setRange(parseInt(val))}
              data={[
                { label: "24H", value: "1" },
                { label: "7D", value: "7" },
                { label: "30D", value: "30" },
                { label: "90D", value: "90" },
              ]}
            />
          </Group>

          <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="md">
            {usage && (
              <>
                <UsageSummary usage={usage} />
                <AgentSummary usage={usage} />
              </>
            )}

            {users && (
              <AnalyticsCard title="Users">
                <BarList
                  customMetric={{
                    label: "users",
                    value: users.length,
                  }}
                  filterZero={false}
                  data={users
                    .sort((a, b) => a.cost - b.cost)
                    .map((u) => ({
                      agentRuns: u.agentRuns,
                      cost: u.cost,
                      barSections: [
                        {
                          value: "cost",
                          tooltip: "Cost",
                          count: u.cost,
                          color: "teal.2",
                        },
                      ],
                      ...u,
                    }))}
                  columns={[
                    {
                      name: "User",
                      render: (u, row) => (
                        <Group my={-4} gap="sm">
                          <AppUserAvatar size={30} user={row} />
                          {formatAppUser(row)}
                        </Group>
                      ),
                    },
                    {
                      name: "Cost",
                      key: "cost",
                      render: formatCost,
                      main: true,
                    },
                  ]}
                />
              </AnalyticsCard>
            )}
          </SimpleGrid>

          {dailyUsage && (
            <>
              <LineChart
                range={range}
                title="Tokens"
                height={230}
                splitBy="name"
                data={dailyUsage
                  .filter((u) => u.type === "llm")
                  .map((p) => ({
                    ...p,
                    tokens: p.completionTokens + p.promptTokens,
                  }))}
                props={["tokens"]}
              />

              <LineChart
                title="Cost Usage"
                range={range}
                height={230}
                formatter={formatCost}
                data={calculateDailyCost(dailyUsage)}
                props={["cost"]}
              />

            </>
          )}
        </Stack>
      </Container>
    </Empty>
  )
}
