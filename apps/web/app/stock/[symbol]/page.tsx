import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { TrendingUp, TrendingDown, DollarSign, BarChart3, Target, Zap } from 'lucide-react'

interface StockPageProps {
  params: {
    symbol: string
  }
}

export default function StockPage({ params }: StockPageProps) {
  const symbol = params.symbol.toUpperCase()
  
  // Mock data - will be replaced with actual API calls
  const mockData = {
    overview: {
      name: symbol === 'TSLA' ? 'Tesla, Inc.' : `${symbol} Corporation`,
      sector: symbol === 'TSLA' ? 'Automotive' : 'Technology',
      currentPrice: symbol === 'TSLA' ? 250.50 : 150.25,
      change: symbol === 'TSLA' ? 5.25 : -2.15,
      changePercent: symbol === 'TSLA' ? 2.14 : -1.41,
      volume: 45000000,
      marketCap: symbol === 'TSLA' ? 800000000000 : 2500000000000
    },
    valuation: {
      fairValue: symbol === 'TSLA' ? 280.75 : 165.50,
      upside: symbol === 'TSLA' ? 12.1 : 10.2,
      pe: symbol === 'TSLA' ? 45.2 : 25.8,
      pePercentile: symbol === 'TSLA' ? 75 : 45
    },
    scenarios: {
      bear: { probability: 15, expectedReturn: -30 },
      sideways: { probability: 25, expectedReturn: 0 },
      base: { probability: 35, expectedReturn: 10 },
      bull: { probability: 20, expectedReturn: 25 },
      hypergrowth: { probability: 5, expectedReturn: 50 }
    }
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              {symbol}
            </h1>
            <p className="text-gray-600 dark:text-gray-300">
              {mockData.overview.name} • {mockData.overview.sector}
            </p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-gray-900 dark:text-white">
              ${mockData.overview.currentPrice.toFixed(2)}
            </div>
            <div className={`flex items-center gap-1 ${
              mockData.overview.change >= 0 ? 'text-green-600' : 'text-red-600'
            }`}>
              {mockData.overview.change >= 0 ? (
                <TrendingUp className="h-4 w-4" />
              ) : (
                <TrendingDown className="h-4 w-4" />
              )}
              <span className="font-medium">
                {mockData.overview.change >= 0 ? '+' : ''}{mockData.overview.change.toFixed(2)} 
                ({mockData.overview.changePercent >= 0 ? '+' : ''}{mockData.overview.changePercent.toFixed(2)}%)
              </span>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-4">
              <div className="text-sm text-muted-foreground">Volume</div>
              <div className="text-lg font-semibold">
                {(mockData.overview.volume / 1000000).toFixed(1)}M
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-sm text-muted-foreground">Market Cap</div>
              <div className="text-lg font-semibold">
                ${(mockData.overview.marketCap / 1000000000).toFixed(0)}B
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-sm text-muted-foreground">P/E Ratio</div>
              <div className="text-lg font-semibold">
                {mockData.valuation.pe}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-sm text-muted-foreground">Fair Value</div>
              <div className="text-lg font-semibold">
                ${mockData.valuation.fairValue.toFixed(2)}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="valuation">Fair Value</TabsTrigger>
          <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
          <TabsTrigger value="news">News</TabsTrigger>
          <TabsTrigger value="peers">Peers</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Price Chart</CardTitle>
                <CardDescription>
                  Historical price action and technical indicators
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[400px] flex items-center justify-center text-muted-foreground">
                  Price chart will be implemented with Recharts
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Key Metrics</CardTitle>
                <CardDescription>
                  Financial and operational metrics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Revenue Growth</span>
                    <span className="font-medium">+15.3%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Gross Margin</span>
                    <span className="font-medium">19.2%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Operating Margin</span>
                    <span className="font-medium">8.7%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">ROE</span>
                    <span className="font-medium">12.4%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Debt/Equity</span>
                    <span className="font-medium">0.15</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="valuation" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Valuation Summary</CardTitle>
                <CardDescription>
                  Multiple valuation models and consensus
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Current Price</span>
                    <span className="font-medium">${mockData.overview.currentPrice.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Fair Value</span>
                    <span className="font-medium text-green-600">${mockData.valuation.fairValue.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Upside/Downside</span>
                    <span className={`font-medium ${mockData.valuation.upside >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {mockData.valuation.upside >= 0 ? '+' : ''}{mockData.valuation.upside.toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">P/E Percentile</span>
                    <Badge variant={mockData.valuation.pePercentile > 70 ? "destructive" : "secondary"}>
                      {mockData.valuation.pePercentile}th
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Valuation Models</CardTitle>
                <CardDescription>
                  Individual model results
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">DCF Model</span>
                    <span className="font-medium">$285.50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Residual Income</span>
                    <span className="font-medium">$275.25</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">PE Percentile</span>
                    <span className="font-medium">$281.00</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">OLS Regression</span>
                    <span className="font-medium">$278.75</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="scenarios" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(mockData.scenarios).map(([scenario, data]) => (
              <Card key={scenario}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="capitalize">{scenario} Case</CardTitle>
                    <Badge variant="secondary">{data.probability}%</Badge>
                  </div>
                  <CardDescription>
                    Expected {scenario} market conditions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">5-Year Return</span>
                      <span className={`font-medium ${
                        data.expectedReturn >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {data.expectedReturn >= 0 ? '+' : ''}{data.expectedReturn}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${data.probability}%` }}
                      ></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Monte Carlo Simulation</CardTitle>
              <CardDescription>
                Probability distribution of future returns
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] flex items-center justify-center text-muted-foreground">
                Monte Carlo simulation chart
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="news" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent News</CardTitle>
              <CardDescription>
                Latest news with sentiment analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">{symbol} Reports Strong Q4 Results</h4>
                    <p className="text-sm text-muted-foreground">Revenue beats expectations by 5%</p>
                  </div>
                  <Badge variant="secondary" className="text-green-600">Positive</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Market Volatility Continues</h4>
                    <p className="text-sm text-muted-foreground">Trading volume remains elevated</p>
                  </div>
                  <Badge variant="secondary" className="text-yellow-600">Neutral</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Analyst Upgrades Price Target</h4>
                    <p className="text-sm text-muted-foreground">Multiple analysts raise targets</p>
                  </div>
                  <Badge variant="secondary" className="text-green-600">Positive</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="peers" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Peer Comparison</CardTitle>
              <CardDescription>
                Comparison with industry peers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Industry Average P/E</h4>
                    <p className="text-sm text-muted-foreground">Technology sector</p>
                  </div>
                  <span className="font-medium">28.5</span>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Revenue Growth vs Peers</h4>
                    <p className="text-sm text-muted-foreground">YoY comparison</p>
                  </div>
                  <span className="font-medium text-green-600">+15.3% vs +8.2%</span>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium">Margin Comparison</h4>
                    <p className="text-sm text-muted-foreground">Gross margin</p>
                  </div>
                  <span className="font-medium text-green-600">19.2% vs 12.8%</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

