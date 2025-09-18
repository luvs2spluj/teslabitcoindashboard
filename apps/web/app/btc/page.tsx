import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react'

export default function BitcoinPage() {
  const btcMetrics = {
    currentPrice: 43250,
    marketCap: 850000000000,
    dominance: 52.3,
    fearGreedIndex: 65,
    cyclePosition: "Early Bull",
    halvingCountdown: 120
  }

  const cycleData = [
    { phase: "Bear Market", duration: "12-18 months", characteristics: "Price decline, low sentiment" },
    { phase: "Accumulation", duration: "6-12 months", characteristics: "Sideways movement, smart money buying" },
    { phase: "Early Bull", duration: "12-18 months", characteristics: "Price recovery, growing adoption" },
    { phase: "Late Bull", duration: "6-12 months", characteristics: "Parabolic growth, FOMO" },
    { phase: "Distribution", duration: "3-6 months", characteristics: "Smart money selling, topping pattern" }
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Bitcoin Analysis
        </h1>
        <p className="text-gray-600 dark:text-gray-300">
          Bitcoin cycle analysis, metrics, and correlation with Tesla and broader markets.
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Bitcoin Price</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${btcMetrics.currentPrice.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              +2.3% from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Market Cap</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(btcMetrics.marketCap / 1000000000).toFixed(0)}B
            </div>
            <p className="text-xs text-muted-foreground">
              Market dominance: {btcMetrics.dominance}%
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Fear & Greed Index</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {btcMetrics.fearGreedIndex}
            </div>
            <p className="text-xs text-muted-foreground">
              Greed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Cycle Position</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {btcMetrics.cyclePosition}
            </div>
            <p className="text-xs text-muted-foreground">
              Days to halving: {btcMetrics.halvingCountdown}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Bitcoin Price History</CardTitle>
            <CardDescription>
              Price action with cycle phases and halving events
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[400px] flex items-center justify-center text-muted-foreground">
              Bitcoin price chart with cycle phases
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>TSLA vs BTC Correlation</CardTitle>
            <CardDescription>
              Rolling correlation between Tesla and Bitcoin prices
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[400px] flex items-center justify-center text-muted-foreground">
              Correlation chart
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Cycle Analysis */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Bitcoin Cycle Analysis</CardTitle>
          <CardDescription>
            Current cycle position and historical patterns
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {cycleData.map((phase, index) => (
              <div key={phase.phase} className="text-center">
                <div className="mb-2">
                  <Badge 
                    variant={index === 2 ? "default" : "secondary"}
                    className="w-full"
                  >
                    {phase.phase}
                  </Badge>
                </div>
                <div className="text-sm text-muted-foreground mb-1">
                  {phase.duration}
                </div>
                <div className="text-xs text-muted-foreground">
                  {phase.characteristics}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Market Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>On-Chain Metrics</CardTitle>
            <CardDescription>
              Key blockchain indicators
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Active Addresses:</span>
                <span className="font-medium">1.2M</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Transaction Volume:</span>
                <span className="font-medium">$8.5B</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Hash Rate:</span>
                <span className="font-medium">450 EH/s</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Difficulty:</span>
                <span className="font-medium">67.3T</span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Market Sentiment</CardTitle>
            <CardDescription>
              Social and market sentiment indicators
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Social Sentiment:</span>
                <span className="font-medium text-green-600">Bullish</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Options Flow:</span>
                <span className="font-medium text-green-600">Call Heavy</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Funding Rate:</span>
                <span className="font-medium">0.01%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">Long/Short Ratio:</span>
                <span className="font-medium">1.8</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
