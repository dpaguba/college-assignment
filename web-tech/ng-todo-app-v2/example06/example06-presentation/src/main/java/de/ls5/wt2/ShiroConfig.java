package de.ls5.wt2;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;

import javax.servlet.Filter;

import de.ls5.wt2.conf.auth.BasicAuthenticationFilterWithoutRedirect;
import de.ls5.wt2.conf.auth.FormAuthenticationFilterWithoutRedirect;
import de.ls5.wt2.conf.auth.LogoutFilterWithoutRedirect;
import de.ls5.wt2.conf.auth.WT2Realm;
import de.ls5.wt2.conf.auth.jwt.JWTAuthenticationFilter;
import de.ls5.wt2.conf.auth.jwt.JWTWT2Realm;
import org.apache.shiro.realm.Realm;
import org.apache.shiro.spring.web.ShiroFilterFactoryBean;
import org.apache.shiro.web.mgt.DefaultWebSecurityManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ShiroConfig {

    @Bean
    public Realm realm() {
        return new WT2Realm();
    }

    @Bean
    public DefaultWebSecurityManager securityManager(Realm realm, Realm jwtRealm) {
        return new DefaultWebSecurityManager(Arrays.asList(jwtRealm, realm));
    }

    @Bean
    public ShiroFilterFactoryBean shiroFilterFactoryBean(DefaultWebSecurityManager securityManager) {

        ShiroFilterFactoryBean shiroFilterFactoryBean = new ShiroFilterFactoryBean();
        shiroFilterFactoryBean.setSecurityManager(securityManager);
        Map<String, Filter> filters = shiroFilterFactoryBean.getFilters();

        filters.put("restAuthenticator", new BasicAuthenticationFilterWithoutRedirect());
        filters.put("loginFilter", new FormAuthenticationFilterWithoutRedirect());
        filters.put("logoutFilter", new LogoutFilterWithoutRedirect());

        final Map<String, String> chainDefinition = new LinkedHashMap<>();

        // configuration for stateless authentication on each request
        chainDefinition.put("/rest/auth/basic/**", "noSessionCreation, restAuthenticator");

        // configuration for using session based authentication
        chainDefinition.put("/login.jsp", "loginFilter");
        chainDefinition.put("/logout", "logoutFilter");

        // configuration for stateless authentication on each request
        chainDefinition.put("/rest/auth/**", "restAuthenticator");

        // make other examples not require authentication
        chainDefinition.put("/rest/**", "anon");

        // make static Angular resources globally available
        chainDefinition.put("/**", "anon");

        shiroFilterFactoryBean.setFilterChainDefinitionMap(chainDefinition);

        return shiroFilterFactoryBean;
    }

}
