'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

export function TeslaScenarios() {
  const scenarios = [
    {
      name: "Bear Case",
      probability: 15,
      description: "Economic downturn, competitive pressure, regulatory headwinds",
      expectedReturn5y: -30,
      expectedReturn10y: -20,
      expectedReturn25y: 0,
      color: "bg-red-500"
    },
    {
      name: "Sideways",
      probability: 25,
      description: "Market consolidation, moderate growth, stable competition",
      expectedReturn5y: 0,
      expectedReturn10y: 5,
      expectedReturn25y: 10,
      color: "bg-yellow-500"
    },
    {
      name: "Base Case",
      probability: 35,
      description: "Normal market conditions, steady growth, manageable competition",
      expectedReturn5y: 10,
      expectedReturn10y: 15,
      expectedReturn25y: 20,
      color: "bg-blue-500"
    },
    {
      name: "Bull Case",
      probability: 20,
      description: "Strong market growth, competitive advantages, favorable regulation",
      expectedReturn5y: 25,
      expectedReturn10y: 30,
      expectedReturn25y: 35,
      color: "bg-green-500"
    },
    {
      name: "Hypergrowth",
      probability: 5,
      description: "Revolutionary technology adoption, market dominance, exponential growth",
      expectedReturn5y: 50,
      expectedReturn10y: 60,
      expectedReturn25y: 70,
      color: "bg-purple-500"
    }
  ]

  const expectedReturns = {
    "5_year": scenarios.reduce((sum, s) => sum + (s.probability / 100) * s.expectedReturn5y, 0),
    "10_year": scenarios.reduce((sum, s) => sum + (s.probability / 100) * s.expectedReturn10y, 0),
    "25_year": scenarios.reduce((sum, s) => sum + (s.probability / 100) * s.expectedReturn25y, 0)
  }

  return (
    <div className="space-y-6">
      {/* Expected Returns Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">5-Year Expected Return</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600">
              {expectedReturns["5_year"].toFixed(1)}%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">10-Year Expected Return</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600">
              {expectedReturns["10_year"].toFixed(1)}%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">25-Year Expected Return</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-600">
              {expectedReturns["25_year"].toFixed(1)}%
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scenario Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {scenarios.map((scenario) => (
          <Card key={scenario.name}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{scenario.name}</CardTitle>
                <Badge variant="secondary" className="text-sm">
                  {scenario.probability}%
                </Badge>
              </div>
              <CardDescription>{scenario.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">5-Year Return:</span>
                  <span className="font-medium">{scenario.expectedReturn5y}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">10-Year Return:</span>
                  <span className="font-medium">{scenario.expectedReturn10y}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">25-Year Return:</span>
                  <span className="font-medium">{scenario.expectedReturn25y}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-4">
                  <div 
                    className={`h-2 rounded-full ${scenario.color}`}
                    style={{ width: `${scenario.probability}%` }}
                  ></div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Monte Carlo Simulation */}
      <Card>
        <CardHeader>
          <CardTitle>Monte Carlo Simulation</CardTitle>
          <CardDescription>
            Probability distribution of future returns based on scenario analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[400px] flex items-center justify-center text-muted-foreground">
            Monte Carlo simulation chart will be implemented with Recharts
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
