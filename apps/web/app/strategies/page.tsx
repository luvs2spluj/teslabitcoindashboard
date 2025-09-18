import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Plus, TrendingUp, Target, Zap } from 'lucide-react'

export default function StrategiesPage() {
  const strategies = [
    {
      name: "SMA Crossover",
      description: "Simple moving average crossover strategy",
      family: "trend_following",
      performance: { sharpe: 1.2, return: 15.3, maxDD: -8.2 }
    },
    {
      name: "MACD + RSI",
      description: "MACD momentum with RSI confirmation",
      family: "momentum",
      performance: { sharpe: 1.8, return: 22.1, maxDD: -12.5 }
    },
    {
      name: "Bollinger Mean Reversion",
      description: "Mean reversion using Bollinger Bands",
      family: "mean_reversion",
      performance: { sharpe: 1.5, return: 18.7, maxDD: -6.8 }
    },
    {
      name: "Momentum + Regime Filter",
      description: "Momentum strategy with regime detection",
      family: "hybrid",
      performance: { sharpe: 2.1, return: 28.4, maxDD: -9.3 }
    }
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Strategy Builder
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Build, test, and optimize trading strategies with comprehensive backtesting tools.
        </p>
      </div>

      <div className="mb-8">
        <Button size="lg">
          <Plus className="mr-2 h-5 w-5" />
          Create New Strategy
        </Button>
      </div>

      {/* Strategy Gallery */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {strategies.map((strategy) => (
          <Card key={strategy.name} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg">{strategy.name}</CardTitle>
                <span className="text-sm text-muted-foreground capitalize">
                  {strategy.family.replace('_', ' ')}
                </span>
              </div>
              <CardDescription>{strategy.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Sharpe Ratio:</span>
                  <span className="font-medium">{strategy.performance.sharpe}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Annual Return:</span>
                  <span className="font-medium text-green-600">
                    {strategy.performance.return}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Max Drawdown:</span>
                  <span className="font-medium text-red-600">
                    {strategy.performance.maxDD}%
                  </span>
                </div>
                <div className="flex gap-2 mt-4">
                  <Button size="sm" variant="outline" className="flex-1">
                    <TrendingUp className="mr-1 h-4 w-4" />
                    Backtest
                  </Button>
                  <Button size="sm" variant="outline" className="flex-1">
                    <Target className="mr-1 h-4 w-4" />
                    Optimize
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Strategy Categories */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Strategy Families</CardTitle>
            <CardDescription>
              Different types of trading strategies available
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Trend Following</h4>
                  <p className="text-sm text-muted-foreground">
                    Strategies that follow market trends
                  </p>
                </div>
                <span className="text-sm text-muted-foreground">3 strategies</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Mean Reversion</h4>
                  <p className="text-sm text-muted-foreground">
                    Strategies that bet on price reversals
                  </p>
                </div>
                <span className="text-sm text-muted-foreground">2 strategies</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Momentum</h4>
                  <p className="text-sm text-muted-foreground">
                    Strategies that ride momentum waves
                  </p>
                </div>
                <span className="text-sm text-muted-foreground">4 strategies</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Hybrid</h4>
                  <p className="text-sm text-muted-foreground">
                    Combination of multiple strategies
                  </p>
                </div>
                <span className="text-sm text-muted-foreground">2 strategies</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Backtests</CardTitle>
            <CardDescription>
              Latest strategy performance results
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">MACD + RSI on TSLA</h4>
                  <p className="text-sm text-muted-foreground">
                    2020-2023 backtest
                  </p>
                </div>
                <span className="text-sm text-green-600 font-medium">+22.1%</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">SMA Crossover on SPY</h4>
                  <p className="text-sm text-muted-foreground">
                    2020-2023 backtest
                  </p>
                </div>
                <span className="text-sm text-green-600 font-medium">+15.3%</span>
              </div>
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium">Bollinger Mean Revert on QQQ</h4>
                  <p className="text-sm text-muted-foreground">
                    2020-2023 backtest
                  </p>
                </div>
                <span className="text-sm text-green-600 font-medium">+18.7%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
