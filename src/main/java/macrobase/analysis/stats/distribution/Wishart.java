package macrobase.analysis.stats.distribution;

import org.apache.commons.math3.linear.EigenDecomposition;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.special.Gamma;

public class Wishart {
    private RealMatrix omega;
    private double nu;
    private int D;  // dimensions

    public Wishart(RealMatrix omega, double nu) {
        this.omega = omega;
        this.nu = nu;
        this.D = omega.getColumnDimension();
    }

    public double lnB() {
        double lnB = -0.5 * nu * Math.log((new EigenDecomposition(omega)).getDeterminant())
                - 0.5 * nu * D * Math.log(2)
                - 0.25 * D * (D - 1) * Math.log(Math.PI);
        for (int i = 1; i <= D; i++) {
            lnB -= Gamma.logGamma(0.5 * (nu + 1 - i));
        }
        return lnB;
    }

    private double expectationLnLambda() {
        double ex_ln_lambda = D * Math.log(2) + Math.log((new EigenDecomposition(omega)).getDeterminant());
        for (int i = 1; i <= D; i++) {
            ex_ln_lambda += Gamma.digamma(0.5 * (nu + 1 - i));
        }
        return ex_ln_lambda;
    }

    public double getEntropy() {
        return -lnB() - 0.5 * (nu - D - 1) * expectationLnLambda() + nu * D / 2.;
    }
}
