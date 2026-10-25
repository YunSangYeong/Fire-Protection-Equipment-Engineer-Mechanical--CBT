"""800 authored numerical variants: 40 declared families × 20 input sets.
All values and idealizations are stated in the stem. No legal design limits,
past-paper claims, current-code claims or external-reference claims.
Generation uses Decimal; tests use independent SI equations in TypeScript.
"""
from decimal import Decimal, ROUND_HALF_UP
D = lambda x: Decimal(str(x))

def fmt(x):
    return format(D(x).normalize(), 'f')

def extend_bank(add, subjects):
    def emit(subject, family, topic, stem, result, unit, values, formula):
        r=D(result).quantize(D('0.01'),rounding=ROUND_HALF_UP)
        # Offset options remain distinct even at the smallest rounded result.
        step=max(D('0.1'),abs(r)*D('0.2')).quantize(D('0.01'),rounding=ROUND_HALF_UP)
        options=[f'{fmt(v)} {unit}' for v in [r,r+step,r-step,r+2*step]]
        add(subject,topic,stem+' 결과는 소수 셋째 자리에서 반올림해 소수 둘째 자리까지 구한다.',options,
            f'문제에서 가정한 조건에 한하여 계산한다. {formula}. 따라서 {fmt(r)} {unit}이다. 표시 단위: {unit}. 실제 화재·설비 설계의 법정 기준, 손실 및 안전 여유를 대신하는 값은 아니다.',
            family,dict(kind=family,values=[float(D(v)) for v in values],result=float(r),unit=unit,precision=2))

    for n in range(1,21):
        # 소방원론: thermodynamics, heat transfer, combustion fundamentals.
        m=D(n+2);c=D('4.2');dt=D(10+n)
        emit(subjects[0],'sensible-heat','현열',f'물 {m} kg을 비열 {c} kJ/(kg·K), 온도 상승 {dt} K로 가열한다. 상변화와 열손실이 없을 때 필요한 열량은?',m*c*dt,'kJ',[m,c,dt],f'Q=mcΔT={m}×{c}×{dt}={m*c*dt} kJ')
        m=D(n)/10;latent=D(2250)
        emit(subjects[0],'latent-heat','상변화 열량',f'포화 상태 물 {m} kg을 같은 온도에서 모두 증발시킨다. 증발잠열을 {latent} kJ/kg으로 가정하면 흡수 열량은?',m*latent,'kJ',[m,latent],f'Q=mL={m}×{latent}={m*latent} kJ')
        rate=D(30+2*n);area=D(n+2)
        emit(subjects[0],'heat-flux','열유속',f'표면 {area} m²에 열 {rate} kW가 균일하게 유입된다. 단위 면적당 열유속은?',rate/area,'kW/m²',[rate,area],f'q″=Q̇/A={rate}/{area}={rate/area} kW/m²')
        ratio=D('1.1')+D(n)/100;initial=D(2)
        emit(subjects[0],'radiation-ratio','복사 방출',f'절대온도가 처음의 {ratio}배가 된 이상 흑체의 표면 복사 방출률을 구한다. 처음 방출률은 {initial} kW/m²이고 주위에서 흡수하는 복사는 무시한다.',initial*ratio**4,'kW/m²',[initial,ratio],f'E=σT⁴이므로 E₂=E₁(T₂/T₁)⁴={initial}×{ratio}⁴={initial*ratio**4} kW/m²')
        k=D('0.5');a=D(n+1);dt=D(40);thickness=D('0.2')
        emit(subjects[0],'wall-conduction','평판 열전도',f'열전도율 {k} W/(m·K), 면적 {a} m², 두께 {thickness} m인 평판의 양면 온도차가 {dt} K다. 1차원 정상 전도 열전달률은?',k*a*dt/thickness,'W',[k,a,dt,thickness],f'Q̇=kAΔT/L={k}×{a}×{dt}/{thickness}={k*a*dt/thickness} W')
        alpha=D('0.000012');length=D(n+4);dt=D(100)
        emit(subjects[0],'linear-expansion','열팽창',f'길이 {length} m인 금속 부재의 선팽창계수는 {alpha} /K다. 구속 없이 온도가 {dt} K 상승하면 길이 증가량은 몇 mm인가?',alpha*length*dt*1000,'mm',[alpha,length,dt],f'ΔL=αLΔT={alpha}×{length}×{dt} m; mm로 환산하면 {alpha*length*dt*1000} mm')
        p=D(100+n);t1=D(300);t2=D(400+n)
        emit(subjects[0],'constant-volume-pressure','이상기체 정적 가열',f'일정한 체적·기체량의 이상기체가 절대압력 {p} kPa, 절대온도 {t1} K에서 {t2} K로 가열된다. 최종 절대압력은?',p*t2/t1,'kPa',[p,t1,t2],f'정적 조건에서 P/T 일정, P₂=P₁T₂/T₁={p}×{t2}/{t1}={p*t2/t1} kPa')
        volume=D(n+5);t1=D(300);t2=D(450)
        emit(subjects[0],'constant-pressure-volume','이상기체 정압 팽창',f'기체량이 일정한 이상기체의 처음 체적은 {volume} L, 절대온도는 {t1} K다. 압력을 일정하게 유지하며 {t2} K로 가열하면 체적은?',volume*t2/t1,'L',[volume,t1,t2],f'정압 조건에서 V/T 일정, V₂=V₁T₂/T₁={volume}×{t2}/{t1}={volume*t2/t1} L')
        total=D(10+n);fraction=D(21)
        emit(subjects[0],'oxygen-volume','혼합기체 체적분율',f'균일한 가상 혼합기체 {total} m³에서 산소 체적분율은 {fraction}%다. 같은 온도·압력 기준으로 산소가 차지하는 환산 체적은?',total*fraction/100,'m³',[total,fraction],f'V산소=V전체×분율={total}×{fraction}/100={total*fraction/100} m³')
        flow=D(n+1)/100;lhv=D(40000)
        emit(subjects[0],'heat-release','연소 열발생률',f'가상 연료가 {flow} kg/s로 완전연소하고 저위발열량이 {lhv} kJ/kg이다. 연소효율을 1로 가정한 열발생률은?',flow*lhv,'kW',[flow,lhv],f'Q̇=ṁH={flow}×{lhv}={flow*lhv} kJ/s={flow*lhv} kW')
        mass=D(10+n);heat=D(20000);area=D(50)
        emit(subjects[0],'fire-load','화재하중 에너지밀도',f'바닥 면적 {area} m² 구역에 발열량 {heat} kJ/kg인 가상 가연물 {mass} kg만 있다. 저장된 연소에너지의 바닥 면적당 값은?',mass*heat/area,'kJ/m²',[mass,heat,area],f'q=mH/A={mass}×{heat}/{area}={mass*heat/area} kJ/m²')
        m1=D(n+1);m2=D(3);t1=D(20);t2=D(80)
        emit(subjects[0],'water-temperature-mix','단열 혼합 열평형',f'물 {m1} kg(온도 {t1} °C)과 물 {m2} kg(온도 {t2} °C)을 단열 용기에서 혼합한다. 두 물의 비열은 같고 상변화·용기 열용량은 무시한다. 평형 온도는?',(m1*t1+m2*t2)/(m1+m2),'°C',[m1,m2,t1,t2],f'열수지에서 T=(m₁T₁+m₂T₂)/(m₁+m₂)=({m1}×{t1}+{m2}×{t2})/({m1}+{m2})={(m1*t1+m2*t2)/(m1+m2)} °C')

        # 소방유체역학: independently named input/output settings.
        rho=D(1000);q=D(n+2)/1000
        emit(subjects[1],'mass-flow','질량유량',f'밀도 {rho} kg/m³인 물이 {q} m³/s로 흐른다. 질량유량은?',rho*q,'kg/s',[rho,q],f'ṁ=ρQ={rho}×{q}={rho*q} kg/s')
        rho=D(1000);q=D('0.01');v1=D(1);v2=D(n+2)
        emit(subjects[1],'momentum-force','직선 유동 운동량',f'물(밀도 {rho} kg/m³)이 {q} m³/s로 정상 흐른다. 직선 방향 평균 속도가 {v1} m/s에서 {v2} m/s로 증가한다. 외력이 유체에 가하는 순힘은? 압력력 등 각 힘을 분해하지 말고 총 외력을 묻는다.',rho*q*(v2-v1),'N',[rho,q,v1,v2],f'정상 운동량 수지 F=ρQ(v₂-v₁)={rho}×{q}×({v2}-{v1})={rho*q*(v2-v1)} N')
        rho=D(1000);v=D(n+1)/2
        emit(subjects[1],'dynamic-pressure','동압',f'밀도 {rho} kg/m³인 물이 {v} m/s로 흐른다. 속도에 대응하는 동압 ρv²/2는?',rho*v*v/2/1000,'kPa',[rho,v],f'p동=ρv²/2={rho}×{v}²/2={rho*v*v/2} Pa={rho*v*v/2/1000} kPa')
        rho=D(1000);v=D(n+1)/10;diameter=D('0.05');mu=D('0.001')
        emit(subjects[1],'reynolds-number','레이놀즈수 계산',f'관 유동의 밀도 {rho} kg/m³, 평균 속도 {v} m/s, 내경 {diameter} m, 점성계수 {mu} Pa·s이다. 레이놀즈수는?',rho*v*diameter/mu,'무차원',[rho,v,diameter,mu],f'Re=ρvD/μ={rho}×{v}×{diameter}/{mu}={rho*v*diameter/mu}')
        f=D('0.02');length=D(10+n);diameter=D('0.1');v=D(2);g=D(10)
        emit(subjects[1],'darcy-loss','직관 마찰손실',f'Darcy 마찰계수 {f}, 관 길이 {length} m, 내경 {diameter} m, 평균 속도 {v} m/s이다. g={g} m/s²로 가정한 직관 마찰손실수두는? 국부손실은 제외한다.',f*length/diameter*v*v/(2*g),'m',[f,length,diameter,v,g],f'h_f=f(L/D)v²/(2g)={f}×({length}/{diameter})×{v}²/(2×{g})={f*length/diameter*v*v/(2*g)} m')
        k=D(n)/10;v=D(3);g=D(10)
        emit(subjects[1],'minor-loss','국부손실',f'밸브 국부손실계수 K={k}, 기준 유속 {v} m/s, g={g} m/s²다. 이 밸브의 국부손실수두만 구하면?',k*v*v/(2*g),'m',[k,v,g],f'h_m=Kv²/(2g)={k}×{v}²/(2×{g})={k*v*v/(2*g)} m')
        re=D(200+40*n)
        emit(subjects[1],'laminar-friction','원관 층류 마찰계수',f'완전 발달한 원관 층류의 레이놀즈수는 {re}이다. Darcy 마찰계수에 1000을 곱한 값은? Fanning 계수가 아님에 유의한다.',64/re*1000,'무차원',[re],f'Darcy f=64/Re이므로 1000f=64000/{re}={64000/re}')
        dp=D(10+n);diameter=D('0.01');mu=D('0.01');length=D(2);pi=D('3.14')
        emit(subjects[1],'poiseuille-flow','층류 원관 체적유량',f'원관 내경 {diameter} m, 길이 {length} m, 압력차 {dp} Pa, 점성계수 {mu} Pa·s이다. 완전 발달 층류로 가정하고 π={pi}를 쓸 때 체적유량은 몇 mL/s인가?',pi*dp*diameter**4/(128*mu*length)*1000000,'mL/s',[dp,diameter,mu,length,pi],f'Q=πΔpD⁴/(128μL)={pi}×{dp}×{diameter}⁴/(128×{mu}×{length}) m³/s; 10⁶을 곱하면 {pi*dp*diameter**4/(128*mu*length)*1000000} mL/s')
        rho=D(1000);vol=D(n+1)/100;g=D(10)
        emit(subjects[1],'buoyancy','정수 중 부력',f'물(밀도 {rho} kg/m³)에 잠긴 물체가 밀어낸 체적이 {vol} m³다. g={g} m/s²일 때 부력 크기는?',rho*g*vol,'N',[rho,g,vol],f'아르키메데스 원리 F_B=ρgV={rho}×{g}×{vol}={rho*g*vol} N')
        r1=D(13600);r2=D(1000);g=D(10);h=D(n+1)/100
        emit(subjects[1],'differential-manometer','차압 마노미터',f'동일 높이 두 물 배관을 U자 액주계로 연결했다. 액주계 액체 밀도 {r1} kg/m³, 물 밀도 {r2} kg/m³, 액면 높이차 {h} m, g={g} m/s²다. 압력차 크기는?',(r1-r2)*g*h/1000,'kPa',[r1,r2,g,h],f'동일 탭 높이에서 Δp=(ρ_m-ρ_w)gh=({r1}-{r2})×{g}×{h} Pa={(r1-r2)*g*h/1000} kPa')
        diameter=D(20+n);pi=D('3.14')
        emit(subjects[1],'pipe-area','원관 단면적',f'원관 내경은 {diameter} mm다. π={pi}를 사용하면 유로 단면적은 몇 cm²인가?',pi*(diameter/10)**2/4,'cm²',[diameter,pi],f'D={diameter}/10 cm, A=πD²/4={pi}×({diameter}/10)²/4={pi*(diameter/10)**2/4} cm²')
        q=D(n+1);diameter=D(50);pi=D('3.14')
        emit(subjects[1],'pipe-velocity','원관 유속',f'물의 유량 {q} L/s, 원관 내경 {diameter} mm다. π={pi}를 사용할 때 평균 유속은?',(q/1000)/(pi*(diameter/1000)**2/4),'m/s',[q,diameter,pi],f'Q={q}/1000 m³/s, D={diameter}/1000 m, v=4Q/(πD²)={(q/1000)/(pi*(diameter/1000)**2/4)} m/s')
        diameter=D(40+4*n)
        emit(subjects[1],'hydraulic-radius','동수반경',f'내경 {diameter} mm인 원관이 물로 가득 차 있다. 젖은 둘레에 대한 유로 면적의 비인 동수반경은?',diameter/4,'mm',[diameter],f'R_h=A/P=(πD²/4)/(πD)=D/4={diameter}/4={diameter/4} mm')
        vol=D(100+n);dp=D(n+1);bulk=D(2000)
        emit(subjects[1],'bulk-compression','체적탄성계수',f'처음 체적 {vol} L인 액체의 체적탄성계수는 {bulk} MPa다. 압력이 {dp} MPa 증가했다. 작은 변화에 대한 선형 근사에서 체적 감소량의 크기는?',vol*dp/bulk,'L',[vol,dp,bulk],f'K=-VΔp/ΔV이므로 감소량 |ΔV|=VΔp/K={vol}×{dp}/{bulk}={vol*dp/bulk} L')

        # 소방기계시설: hypothetical equipment calculations, not legal limits.
        water=D(n+5);eta=D('0.8')
        emit(subjects[3],'shaft-power','펌프 축동력',f'펌프 수동력이 {water} kW, 효율이 {eta}다. 필요한 축동력은?',water/eta,'kW',[water,eta],f'η=P수/P축이므로 P축=P수/η={water}/{eta}={water/eta} kW')
        water=D(n+5);shaft=D(n+15)
        emit(subjects[3],'pump-efficiency','펌프 효율',f'펌프 수동력 {water} kW, 축동력 {shaft} kW다. 펌프 효율을 백분율로 나타내면?',water/shaft*100,'%',[water,shaft],f'η=100P수/P축=100×{water}/{shaft}={water/shaft*100}%')
        q=D(100+5*n);n1=D(1000);n2=D(1200)
        emit(subjects[3],'affinity-flow','펌프 상사 유량',f'같은 임펠러의 펌프가 {n1} rpm에서 유량 {q} L/min이다. 상사법칙이 성립한다고 가정하고 {n2} rpm으로 바꾸면 대응 유량은?',q*n2/n1,'L/min',[q,n1,n2],f'같은 임펠러 상사점에서 Q₂/Q₁=N₂/N₁; Q₂={q}×{n2}/{n1}={q*n2/n1} L/min')
        h=D(10+n);n1=D(1000);n2=D(1500)
        emit(subjects[3],'affinity-head','펌프 상사 양정',f'같은 임펠러 펌프의 {n1} rpm 상사점 양정은 {h} m다. {n2} rpm 상사점의 양정은? 손실·효율 변화는 무시한다.',h*(n2/n1)**2,'m',[h,n1,n2],f'H₂/H₁=(N₂/N₁)²; H₂={h}×({n2}/{n1})²={h*(n2/n1)**2} m')
        power=D(n+2);n1=D(1000);n2=D(1200)
        emit(subjects[3],'affinity-power','펌프 상사 동력',f'펌프가 {n1} rpm 상사점에서 축동력 {power} kW를 소비한다. 동일 임펠러·같은 효율의 상사법칙으로 {n2} rpm 상사점 동력을 구하면?',power*(n2/n1)**3,'kW',[power,n1,n2],f'P₂/P₁=(N₂/N₁)³; P₂={power}×({n2}/{n1})³={power*(n2/n1)**3} kW')
        k=D(30+n);p=D(4)
        emit(subjects[3],'nozzle-k','노즐 방수계수',f'가상 노즐의 방수식은 Q=K√p다. Q 단위 L/min, p 단위 bar, K={k} L/(min·√bar)이다. p={p} bar일 때 방수량은?',k*p.sqrt(),'L/min',[k,p],f'문제의 계수 단위를 그대로 적용하여 Q=K√p={k}×√{p}={k*p.sqrt()} L/min')
        count=D(n+1);q=D(40)
        emit(subjects[3],'parallel-outlet-flow','동시 방수 합계',f'각 방출구가 모두 {q} L/min을 방수한다. 방출구 {count}개가 동시에 작동할 때 총 유량은? 모든 방출구의 유량이 유지된다고 가정한다.',count*q,'L/min',[count,q],f'총유량은 독립 유량의 합 Q총=Nq={count}×{q}={count*q} L/min')
        q=D(100+10*n);area=D(20)
        emit(subjects[3],'spray-density','평균 살수밀도',f'가상 살수 구역 {area} m²에 총 {q} L/min이 균일하게 방수된다. 평균 살수밀도는? 실제 설치기준의 요구밀도와 무관한 산술 문제다.',q/area,'L/(min·m²)',[q,area],f'd=Q/A={q}/{area}={q/area} L/(min·m²)')
        volume=D(200+20*n);fraction=D(6)
        emit(subjects[3],'foam-water-volume','포 혼합용 물량',f'가상 포 수용액 최종 {volume} L를 원액 체적비 {fraction}%로 혼합한다. 체적이 가산된다고 가정하면 물은 몇 L 필요한가? 지정 혼합비를 제시하는 문제가 아니다.',volume*(1-fraction/100),'L',[volume,fraction],f'물량=최종량×(1-원액비)={volume}×(1-{fraction}/100)={volume*(1-fraction/100)} L')
        a=D(2);b=D(3);h=D(n+1)/10
        emit(subjects[3],'rectangular-tank','직육면체 수조 유효체적',f'가상 수조의 내부 바닥 가로 {a} m, 세로 {b} m, 실제 물 깊이 {h} m다. 내부 장애물은 없다고 할 때 물의 체적은 몇 L인가? 법정 유효수량 산정이 아닌 기하 문제다.',a*b*h*1000,'L',[a,b,h],f'V=abh={a}×{b}×{h} m³; 1 m³=1000 L이므로 {a*b*h*1000} L')
        r=D('0.5');h=D(n+1)/10;pi=D('3.14')
        emit(subjects[3],'cylindrical-tank','원통 수조 체적',f'수직 원통 수조의 내부 반지름은 {r} m, 물 깊이는 {h} m다. π={pi}로 가정하면 저장된 물의 기하학적 체적은 몇 L인가?',pi*r*r*h*1000,'L',[r,h,pi],f'V=πr²h={pi}×{r}²×{h} m³; L로 환산하면 {pi*r*r*h*1000} L')
        pressure=D(100+10*n);area=D('0.002')
        emit(subjects[3],'pressure-force','밸브 면 압력힘',f'밸브의 평평한 유효면적 {area} m²에 차압 {pressure} kPa가 균일하게 작용한다. 이 차압에 의한 힘의 크기는? 스프링과 마찰은 제외한다.',pressure*1000*area,'N',[pressure,area],f'F=ΔpA={pressure}×1000×{area}={pressure*1000*area} N')
        beta=D('0.001');volume=D(10+n);dt=D(50)
        emit(subjects[3],'liquid-thermal-expansion','감열액 팽창 모형',f'가상 감열액의 처음 체적은 {volume} mL, 체적팽창계수는 {beta} /K다. 온도가 {dt} K 상승할 때 작은 변화 근사로 체적 증가량은? 실제 헤드의 작동온도나 압력을 묻지 않는다.',beta*volume*dt,'mL',[beta,volume,dt],f'ΔV=βVΔT={beta}×{volume}×{dt}={beta*volume*dt} mL')
        p1=D(400+10*n);volume=D(5);p2=D(200)
        emit(subjects[3],'isothermal-gas-volume','압축기체 등온 모형',f'가상 이상기체 {volume} L의 처음 절대압력은 {p1} kPa다. 기체량·온도를 일정하게 유지하여 절대압력을 {p2} kPa로 낮추면 체적은? 실제 소화약제 저장·방출량 산정이 아닌 이상기체 모형이다.',p1*volume/p2,'L',[p1,volume,p2],f'등온 이상기체에서 P₁V₁=P₂V₂; V₂={p1}×{volume}/{p2}={p1*volume/p2} L')
