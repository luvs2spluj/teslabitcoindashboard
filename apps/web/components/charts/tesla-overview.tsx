'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, TrendingDown, DollarSign, Car } from 'lucide-react'

export function TeslaOverview() {
  // Mock data - will be replaced with actual API calls
  const mockData = {
    latestMetrics: {
      vehicles_delivered: 484507,
      asp_auto: 47300,
      auto_gross_margin: 0.19,
      energy_solar_mw: 66,
      energy_storage_mwh: 2959,
      energy_gross_margin: 0.24
    },
    deliveryTrend: [
      { date: '2023-Q1', vehicles_delivered: 422875 },
      { date: '2023-Q2', vehicles_delivered: 466140 },
      { date: '2023-Q3', vehicles_delivered: 435059 },
      { date: '2023-Q4', vehicles_delivered: 484507 }
    ],
    marginTrend: [
      { date: '2023-Q1', auto_gross_margin: 0.19, energy_gross_margin: 0.24 },
      { date: '2023-Q2', auto_gross_margin: 0.18, energy_gross_margin: 0.24 },
      { date: '2023-Q3', auto_gross_margin: 0.18, energy_gross_margin: 0.24 },
      { date: '2023-Q4', auto_gross_margin: 0.19, energy_gross_margin: 0.24 }
    ]
  }

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Vehicles Delivered</CardTitle>
            <Car className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockData.latestMetrics.vehicles_delivered.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              Q4 2023
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">ASP Automotive</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${mockData.latestMetrics.asp_auto.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              Average selling price
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Auto Gross Margin</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {(mockData.latestMetrics.auto_gross_margin * 100).toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">
              Q4 2023
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Energy Storage</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {mockData.latestMetrics.energy_storage_mwh.toLocaleString()} MWh
            </div>
            <p className="text-xs text-muted-foreground">
              Q4 2023
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Vehicle Deliveries Trend</CardTitle>
            <CardDescription>
              Quarterly vehicle deliveries over time
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-muted-foreground">
              Chart will be implemented with Recharts
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Gross Margins</CardTitle>
            <CardDescription>
              Automotive and Energy gross margins
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center text-muted-foreground">
              Chart will be implemented with Recharts
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recent News */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Tesla News</CardTitle>
          <CardDescription>
            Latest news and sentiment analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Tesla Reports Q4 2023 Results</h4>
                <p className="text-sm text-muted-foreground">Record deliveries and strong margins</p>
              </div>
              <span className="text-sm text-green-600">Positive</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">Cybertruck Production Update</h4>
                <p className="text-sm text-muted-foreground">Production ramp and delivery timeline</p>
              </div>
              <span className="text-sm text-green-600">Positive</span>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-medium">FSD Beta v12 Release</h4>
                <p className="text-sm text-muted-foreground">Latest autonomous driving improvements</p>
              </div>
              <span className="text-sm text-blue-600">Neutral</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
