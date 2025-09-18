import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { TrendingUp, BarChart3, Target, Zap } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Financial App
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Tesla-focused financial analysis with comprehensive data, valuation models, 
            scenario analysis, and strategy backtesting tools.
          </p>
          <div className="flex gap-4 justify-center">
            <Button asChild size="lg">
              <Link href="/tsla">
                <TrendingUp className="mr-2 h-5 w-5" />
                Tesla Dashboard
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/strategies">
                <Target className="mr-2 h-5 w-5" />
                Strategy Builder
              </Link>
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <Card>
            <CardHeader>
              <TrendingUp className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle>Tesla Analysis</CardTitle>
              <CardDescription>
                Comprehensive Tesla metrics including vehicles, energy, and margins
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full">
                <Link href="/tsla">View Dashboard</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <BarChart3 className="h-8 w-8 text-green-600 mb-2" />
              <CardTitle>Valuation Models</CardTitle>
              <CardDescription>
                DCF, OLS regression, and scenario analysis for fair value
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full">
                <Link href="/stock/tsla">Analyze Stock</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Target className="h-8 w-8 text-purple-600 mb-2" />
              <CardTitle>Strategy Backtesting</CardTitle>
              <CardDescription>
                Build and test trading strategies with optimization
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full">
                <Link href="/strategies">Build Strategy</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <Zap className="h-8 w-8 text-orange-600 mb-2" />
              <CardTitle>Bitcoin Analysis</CardTitle>
              <CardDescription>
                Bitcoin cycle analysis and correlation with Tesla
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button asChild variant="outline" className="w-full">
                <Link href="/btc">View BTC</Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Quick Links */}
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Quick Access
          </h2>
          <div className="flex flex-wrap gap-4 justify-center">
            <Button asChild variant="secondary">
              <Link href="/stock/tsla">TSLA Analysis</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/compare">Benchmark Compare</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/backtests">Recent Backtests</Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/btc">Bitcoin Metrics</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
